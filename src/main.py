import typer
import subprocess
import os
from pathlib import Path

from src.constants import PATH_TO_ROOT

from src.analyzer import MainAnalyzer
from src.render import Render
from src.singleton import Singleton
from src.default_class import Stage, Job

app = typer.Typer()


@app.command()
def main(
    link: str,
    dir: Path | None = None,
    test: bool = False
):
    singleton = Singleton()
    singleton.test = test

    if dir is None:
        dir = Path(os.getcwd()) / link.rsplit('/', 1)[-1]
    if (dir / '.git').exists():
        print("* Repo already exists. Skipping git clone")
    else:
        print("* Attempting to clone repo...")
        command = ["git", "clone", link, dir]
        subprocess.run(command)

    if test:
        singleton.stages["checkout"] = Stage("checkout")
        singleton.stages["checkout"].jobs.append(Job(
            "checkout",
            f"""scmGit(
            branches: [[name: 'master']],
            userRemoteConfigs: [[url: 'file:///var/jenkins_home/test/{dir.name}']])
            """
        ))

    os.chdir(dir)

    main_analyzer = MainAnalyzer()
    main_analyzer.load_languages()
    main_analyzer.analyze()
    main_analyzer.build()
    os.chdir(PATH_TO_ROOT)

    render = Render()
    result = render.render()

    print()
    print("### Jenkinsfile ###\n")
    print(result)


if __name__ == "__main__":
    app()

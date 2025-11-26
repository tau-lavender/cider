import typer
import subprocess
import os
from pathlib import Path

from src.constants import PATH_TO_ROOT

from src.analyzer import MainAnalyzer
from src.render import Render

app = typer.Typer()


@app.command()
def main(
    link: str,
    dir: Path | None = None,
):
    if dir is None:
        dir = Path(os.getcwd()) / link.rsplit('/', 1)[-1]
    if (dir / '.git').exists():
        print("* Repo already exists. Skipping git clone")
    else:
        print("* Attempting to clone repo...")
        command = ["git", "clone", link, dir]
        subprocess.run(command)

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

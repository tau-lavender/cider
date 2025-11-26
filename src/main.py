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
    dir: Path = ".",
    ):
    
    print(link, dir)

    if not dir.exists():
        os.mkdir(dir)
    subprocess.run(["git", "clone", link, dir])
    os.chdir(dir)

    main_analyzer = MainAnalyzer()
    main_analyzer.load_languages()
    main_analyzer.analyze()
    main_analyzer.build()
    os.chdir(PATH_TO_ROOT)

    render = Render()
    result = render.render()
    print(result)


    # TODO
    # Build


if __name__ == "__main__":
    app()

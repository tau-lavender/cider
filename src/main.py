import typer
import subprocess
import os
from pathlib import Path

from src.constants import PATH_TO_ROOT

from src.analyzer import MainAnalyzer

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

    # TODO
    # create class Analyzer
    main_analyzer = MainAnalyzer()
    main_analyzer.load_languages()

    main_analyzer.analyze()

    os.chdir(PATH_TO_ROOT)

    # TODO
    # Build


if __name__ == "__main__":
    app()

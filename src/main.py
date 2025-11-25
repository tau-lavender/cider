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
    if not(dir.exists()):
        os.mkdir(dir)
    os.chdir(dir)
    subprocess.run(f"git clone {link}")
    os.chdir(PATH_TO_ROOT)

    # TODO
    # create class Analyzer 
    main_analyzer = MainAnalyzer()
    MainAnalyzer.analyze()

    # TODO
    # Build


if __name__ == "__main__":
    app()

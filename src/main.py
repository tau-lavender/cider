import typer
import subprocess
import os
from pathlib import Path

from src.constants import PATH_TO_ROOT


app = typer.Typer()

@app.command()
def main(
    link: str,
    dir: Path = ".",
):
    print(link, dir)
    try:
        if not(dir.exists()):
            os.mkdir(dir)
        os.chdir(dir)
        subprocess.run(f"git clone {link}")
        os.chdir(PATH_TO_ROOT)
    except OSError as e:
        print(f"OSError: {e}")

if __name__ == "__main__":
    try:
        app()
    except OSError as e:
        print(f"OSError: {e}")

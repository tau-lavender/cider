from src.default_class import Framework

from pathlib import Path

from src.singleton import Singleton
from src.default_class import Job


class FlaskFramework(Framework):
    def __init__(self):
        super().__init__()
        self.name = "Flask"

        self.flask_found = False
        self.app_file = ""

    def analyze(self, file_path: Path, file_contents: str):
        if (
            "from flask import Flask" in file_contents
            or "import flask" in file_contents
        ):
            self.flask_found = True

        if self.flask_found and (
            "create_app(" in file_contents
        ):
            self.app_file = file_path

    def build(self):
        singleton = Singleton()
        if self.app_file:
            run_job = Job(runner="", command="")
            singleton.stages["deploy"].append(run_job)

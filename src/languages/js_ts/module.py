from src.default_class import (
    Language,
    Job
)

from enum import Enum, auto
from pathlib import Path

from src.singleton import Singleton

from src.languages.go.config import FRAMEWORK_IMPORT_CONFIG


class JsLanguage(Language):
    def __init__(self):
        super().__init__()
        self.name = "JS/TS"
        self.masks: set = {
            "*.jsx",
            "*.tsx",
            "*.js",
            "*.ts",
            "package.json",
        }
        self.framework_config = FRAMEWORK_IMPORT_CONFIG

        self.found_package_json = False

    def analyze(self, file_path: Path):
        with open(file_path, "r") as file:
            file_contents = file.read()

        # TODO: figure out which script to run from package.json
        # TODO: install yarn if its used in script

        for framework in self.frameworks:
            framework.analyze(file_path, file_contents)

    def build(self):
        singleton = Singleton()

        for framework in self.frameworks:
            framework.build()

        # TODO: figure out which script to run from package.json
        # go_run_job = Job("sh", "npm run prod")
        # singleton.stages["deploy"].jobs.insert(0, go_run_job)

from src.default_class import (
    Language,
    Job
)

from enum import Enum, auto
from pathlib import Path

from src.singleton import Singleton

from src.languages.go.config import FRAMEWORK_IMPORT_CONFIG

import json


class DependenceManager(Enum):
    NPM = auto()
    YARN = auto()


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
            "yarn.lock",
        }
        self.framework_config = FRAMEWORK_IMPORT_CONFIG

        self.dependence_manager: DependenceManager = DependenceManager.NPM
        self.tests = False

    def analyze(self, file_path: Path):
        with open(file_path, "r") as file:
            file_contents = file.read()

        if file_path.name == "yarn.lock":
            self.dependence_manager = DependenceManager.YARN

        if file_path.name == "package.json":
            package = json.loads(file_contents)
            scripts = package['scripts']
            if "test" in scripts.keys():
                self.tests = True
                print("* Detected `test` script")

        for framework in self.frameworks:
            framework.analyze(file_path, file_contents)

    def build(self):
        singleton = Singleton()

        for framework in self.frameworks:
            framework.build()

        if self.dependence_manager == DependenceManager.YARN:
            print("* Detected Yarn")
            yarn_job = Job("sh", "npm install --global yarn")
            singleton.stages["build"].jobs.insert(0, yarn_job)

            install_job = Job("sh", "yarn install")
            singleton.stages["build"].jobs.insert(1, install_job)

            build_job = Job("sh", "yarn build")
            singleton.stages["build"].jobs.insert(2, build_job)

            if self.tests:
                test_job = Job("sh", "yarn test")
                singleton.stages["test"].jobs.append(test_job)
        else:
            print("* Detected NPM")
            install_job = Job("sh", "npm install")
            singleton.stages["build"].jobs.insert(0, install_job)

            build_job = Job("sh", "npm run build")
            singleton.stages["build"].jobs.insert(1, build_job)

            if self.tests:
                test_job = Job("sh", "npm run test")
                singleton.stages["test"].jobs.append(test_job)

        server_job = Job("sh", "node server")
        singleton.stages["deploy"].jobs.append(server_job)

from src.default_class import (
    Language,
    Job
)

from pathlib import Path

from src.singleton import Singleton

from src.languages.go.config import FRAMEWORK_IMPORT_CONFIG


class GoLanguage(Language):
    def __init__(self):
        super().__init__()
        self.name = "Java/Kotlin"
        self.masks: set = {
            "*.java",
            "*.kotlin",
        }
        self.framework_config = FRAMEWORK_IMPORT_CONFIG

    def analyze(self, file_path: Path):
        with open(file_path, "r") as file:
            file_contents = file.read()

        for framework in self.frameworks:
            framework.analyze(file_path, file_contents)

    def build(self):
        singleton = Singleton()

        for framework in self.frameworks:
            framework.build()

        # build
        # TODO: maybe we dont need get sometimes
        go_get_job = Job("sh", "go get .")
        go_build_job = Job("sh", "go build -o executable")
        singleton.stages["build"].jobs.insert(0, go_get_job)
        singleton.stages["build"].jobs.insert(1, go_build_job)

        # deploy
        ext = ""
        # if sys.platform == "win32":
        #     ext = ".exe"

        go_run_job = Job("sh", f"./executable{ext}")
        singleton.stages["deploy"].jobs.insert(0, go_run_job)

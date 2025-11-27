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

        install_job = Job("sh", "mvn install")
        build_job = Job("sh", "mvn -B -DskipTests -Djar.finalName=output clean package")
        singleton.stages["build"].jobs.insert(0, install_job)
        singleton.stages["build"].jobs.insert(1, build_job)

        test_job = Job("sh", "mvn test")
        print("* Detected tests")
        singleton.stages["test"].jobs.insert(1, test_job)

        run_job = Job("sh", "java -jar target/output.jar")
        singleton.stages["deploy"].jobs.insert(0, run_job)

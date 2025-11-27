from src.default_class import Framework

from pathlib import Path

from src.singleton import Singleton
from src.default_class import Job


class PytestFramework(Framework):
    def __init__(self):
        super().__init__()
        self.name = "Pytest"

        self.pytest_found = False

    def analyze(self, file_path: Path, file_contents: str):
        if not self.pytest_found:
            if (
                (file_path.name.startswith("test_") or file_path.name.endswith("_test.py"))
                and ("test_" in file_contents or "_test(" in file_contents)
            ):
                self.pytest_found = True

    def build(self):
        singleton = Singleton()
        if self.pytest_found:
            print("* Detected Pytest")
            run_job = Job(runner="sh", command="pytest")
            run_job.tags.add('python')
            singleton.stages["test"].jobs.append(run_job)

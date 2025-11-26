from src.default_class import Framework

from pathlib import Path

from src.singleton import Singleton
from src.default_class import Job


class TestFramework(Framework):
    def __init__(self):
        super().__init__()
        self.name = "Test"

        self.test_found = False

    def analyze(self, file_path: Path, file_contents: str):
        if not self.test_found:
            if file_path.name.endswith("_test.go"):
                self.test_found = True

    def build(self):
        singleton = Singleton()
        if self.test_found:
            run_job = Job(runner="sh", command="go test")
            singleton.stages["test"].jobs.append(run_job)

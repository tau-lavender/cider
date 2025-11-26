from src.default_class import Framework

from pathlib import Path

from src.singleton import Singleton
from src.default_class import Job


class FastapiFramework(Framework):
    def __init__(self):
        super().__init__()
        self.name = "FastAPI"

        self.fastapi_found = False
        self.fastapi_file: Path = None

    def analyze(self, file_path: Path, file_contents: str):
        if not self.fastapi_found:
            if (
                "from fastapi import FastAPI " in file_contents
                or "import fastapi" in file_contents
            ):
                self.fastapi_found = True

        if "app = FastAPI(" in file_contents:
            self.fastapi_file = file_path

    def build(self):
        singleton = Singleton()
        if self.fastapi_found:
            run_job = Job(runner="sh", command=f"fastapi run {self.fastapi_file}")
            run_job.tags.add('python')
            singleton.stages["deploy"].jobs.append(run_job)

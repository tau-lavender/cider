from src.default_class import Framework

from pathlib import Path

from src.singleton import Singleton
from src.default_class import Job


class PytestFramework(Framework):
    def __init__(self):
        super().__init__()
        self.name = "Django"

        self.django_found = False

    def analyze(self, file_path: Path, file_contents: str):
        if not self.django_found:
            if ("import django" in file_contents
                or "from django" in file_contents):
                self.django_found = True

    def build(self):
        singleton = Singleton()
        if self.django_found:
            print("* Detected Django")
            run_job = Job(runner="sh", command="python manage.py runserver")
            run_job.tags.add('python')
            singleton.stages["test"].jobs.append(run_job)

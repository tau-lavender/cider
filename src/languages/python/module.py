from src.default_class import (
    Language,
    Job
)

from enum import Enum, auto
from pathlib import Path

from src.singleton import Singleton

from src.languages.python.config import FRAMEWORK_IMPORT_CONFIG


class DependenceManager(Enum):
    NO_MANAGER = auto()
    UV = auto()
    POETRY = auto()
    REQUIREMENTS = auto()


class PythonLanguage(Language):
    def __init__(self):
        super().__init__()
        self.name = "Python"
        self.masks: set = {
            "*.py",
            "pyproject.toml",
            "requirements.txt"
            "uv.lock",
        }
        self.framework_config = FRAMEWORK_IMPORT_CONFIG

        self.requires_python = ""
        self.dependence_manager: DependenceManager = DependenceManager.NO_MANAGER

    def analyze(self, file_path: Path):
        with open(file_path, "r") as file:
            file_contents = file.read()
        if file_path.name == "pyproject.toml":
            if "requires-python" in file_contents:
                pass

        for framework in self.frameworks:
            framework.analyze(file_path, file_contents)

    def build(self):
        # TODO: если будет время добавить рендер докера
        for framework in self.frameworks:
            framework.build()
        singleton = Singleton()
        match self.dependence_manager:
            case DependenceManager.NO_MANAGER:
                pass
            case DependenceManager.UV:
                uv_venv_job = Job("sh", "uv venv")
                uv_sync_job = Job("sh", "uv sync")
                singleton.stages["build"].jobs.insert(0, uv_venv_job)
                singleton.stages["build"].jobs.insert(1, uv_sync_job)

                # обёртка команд в "uv run"
                for stage in singleton.stages.values():
                    for job in stage.jobs:
                        if "python" in job.tag:
                            job.command = "uv run " + job.command
            case DependenceManager.POETRY:
                install_poetry_job = Job("sh", "pip vinstall poetry]")
                install_dependences_job = Job("sh", "poetry install")
                singleton.stages["build"].jobs.insert(0, install_poetry_job)
                singleton.stages["build"].jobs.insert(1, install_dependences_job)

                # обёртка команд в "poetry run"
                for stage in singleton.stages.values():
                    for job in stage.jobs:
                        if "python" in job.tag:
                            job.command = "poetry run " + job.command
            case DependenceManager.REQUIREMENTS:
                install_requirements_job = Job("sh", "pip install -r requirements.txt")
                singleton.stages["build"].jobs.insert(0, install_requirements_job)

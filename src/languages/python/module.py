from src.default_class import (
    Language,
    Job
)

from singleton import Singleton

from enum import Enum, auto
from pathlib import Path

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
        self.start_cmd: str | None = None

    def analyze(self, file_path: Path):
        with open(file_path, "r") as file: 
            file_contents = file.read()
        if file_path.name == "pyproject.toml":
            if "requires-python" in file_contents:
                pass
                
        for framework in self.frameworks:
            framework.analyze(file_path, file_contents)

    def build(self):
        for framework in self.frameworks:
            framework.build()
        singleton = Singleton()
        match self.dependence_manager:
            case DependenceManager.NO_MANAGER:
                # TODO: start default python

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

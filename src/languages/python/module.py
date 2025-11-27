from src.default_class import (
    Language,
    Job
)

from string import digits
from enum import Enum, auto
from pathlib import Path
import os

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
            "requirements.txt",
            "uv.lock",
        }
        self.framework_config = FRAMEWORK_IMPORT_CONFIG

        self.requires_python = ""
        self.main_file_name = None
        self.dependence_manager: DependenceManager = DependenceManager.NO_MANAGER

    def find_requires_python(self, file_contents: str):
        if "requires-python" in file_contents:
            py_ver = file_contents[file_contents.find("requires-python"):]
            py_ver = py_ver[: py_ver.find('\n')]
            py_ver = py_ver[py_ver.find('"'): py_ver.rfind('"')]
            for symbol in py_ver:
                if symbol in digits + '.':
                    self.requires_python += symbol
        # print(self.requires_python)

    def analyze(self, file_path: Path):
        with open(file_path, "r") as file:
            file_contents = file.read()
        if file_path.name == "pyproject.toml":
            self.find_requires_python(file_contents)

        if file_path.name == "uv.lock":
            self.find_requires_python(file_contents)
            self.dependence_manager = DependenceManager.UV
        elif file_path.name == "poetry.lock":
            self.find_requires_python(file_contents)
            self.dependence_manager = DependenceManager.POETRY
        elif file_path.name == "requirements.txt" and self.dependence_manager == DependenceManager.NO_MANAGER:
            self.dependence_manager = DependenceManager.REQUIREMENTS


        if file_path.name in ("main.py", "_main_.py", "__main__.py"):
            self.main_file_name = str(os.path.relpath(file_path, os.getcwd())).replace("\\", ".")[:-3]

        for framework in self.frameworks:
            framework.analyze(file_path, file_contents)

    def build(self):
        # TODO: если будет время добавить рендер докера
        for framework in self.frameworks:
            framework.build()

        singleton = Singleton()
        
        if not singleton.stages["deploy"].jobs:
            default_job = Job("sh", f"python -m {self.main_file_name}")
            singleton.stages["deploy"].jobs.append(default_job)


        match self.dependence_manager:
            case DependenceManager.NO_MANAGER:
                print("* Python dependency manager not detected")

            case DependenceManager.UV:
                print("* Detected python dependency manager: uv")

                uv_venv_job = Job("sh", "uv venv")
                uv_sync_job = Job("sh", "uv sync")
                singleton.stages["build"].jobs.insert(0, uv_venv_job)
                singleton.stages["build"].jobs.insert(1, uv_sync_job)

                # обёртка команд в "uv run"
                for stage in singleton.stages.values():
                    for job in stage.jobs:
                        if "python" in job.tags:
                            job.command = "uv run " + job.command
            
            case DependenceManager.POETRY:
                print("* Detected python dependency manager: poetry")

                install_poetry_job = Job("sh", "pip vinstall poetry]")
                install_dependences_job = Job("sh", "poetry install")
                singleton.stages["build"].jobs.insert(0, install_poetry_job)
                singleton.stages["build"].jobs.insert(1, install_dependences_job)

                # обёртка команд в "poetry run"
                for stage in singleton.stages.values():
                    for job in stage.jobs:
                        if "python" in job.tags:
                            job.command = "poetry run " + job.command
            
            case DependenceManager.REQUIREMENTS:
                print("* Detected python dependency manager: requirements.txt")

                install_requirements_job = Job("sh", "pip install -r requirements.txt")
                singleton.stages["build"].jobs.insert(0, install_requirements_job)

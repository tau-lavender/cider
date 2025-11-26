from src.default_class import (
    Framework,
    Language
)

import importlib
import inspect

from pathlib import Path

from src.languages.python.config import FRAMEWORK_IMPORT_CONFIG


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

    def analyze(self, file: Path):
        for framework in self.frameworks:
            framework.analyze(file)

    def build(self):
        """
        """

        pass

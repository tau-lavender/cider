from src.default_class import Framework

from pathlib import Path


class FlaskFramework(Framework):
    def __init__(self):
        super().__init__()
        self.name = "Flask"

    def analyze(self, path: Path):
        if True:
            pass

    def build(self):
        pass

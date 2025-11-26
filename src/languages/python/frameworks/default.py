from src.default_class import Framework

from pathlib import Path


class NoFramework(Framework):
    def __init__(self):
        super().__init__()
        self.name = "No Framework"

    def analyze(self, file_path: Path, file_contents: str):
        # TODO
        # check imports
        if True:
            self.project_data.add("python") #set

    def build(self):
        if "python" in self.project_data:
            pass # add python start

        pass

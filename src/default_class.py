import importlib
import inspect


class Framework():
    def __init__(self):
        self.project_data = set()
        self.name = "Base Framework"

    def analyze(self):
        pass

    def build(self):
        pass


class Language():
    def __init__(self):
        self.masks: set = set()
        self.frameworks: list[Framework] = []
        self.framework_config: list[str] = []

    def load_frameworks(self):
        for plugin_name in self.framework_config:
            mod = importlib.import_module(plugin_name)
            classes = inspect.getmembers(mod, inspect.isclass)
            for framework in classes:
                if not issubclass(Framework, framework[1]) and issubclass(framework[1], Framework):
                    self.frameworks.append(framework[1]())

    def analyze(self):
        pass

    def build(self):
        pass


class Job():
    def __init__(self, runner: str, command: str):
        self.runner: str = ""
        self.command: str = ""


class Stage():
    def __init__(self, name: str):
        self.name = name
        self.jobs: list[Job] = []
        self.image: str = ""

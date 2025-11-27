from src.default_class import Stage


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


@singleton
class Singleton():
    def __init__(self):
        self.stages: dict[str, Stage] = {}
        self.init_stages()

    def init_stages(self):
        self.stages["build"] = Stage("build")
        self.stages["test"] = Stage("test")
        self.stages["deploy"] = Stage("deploy")

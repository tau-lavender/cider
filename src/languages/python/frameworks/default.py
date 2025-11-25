from src.default_class import Framework


class DefFramework(Framework):
    def __init__(self):
        super().__init__()

    def analyze(self):
        # TODO
        # check imports
        if True:
            self.project_data.add("python") #set

    def build(self):
        if "python" in self.project_data:
            pass # add python start

        pass

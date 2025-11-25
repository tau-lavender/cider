from src.framework import Framework


class Language():
    def __init__(self):
        self.masks: set = set()
        self.frameworks: list[Framework] = []

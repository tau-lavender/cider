from src.analyzer import Analyzer
from src.default_class import Builder


class Framework():
    def __init__(self, analyzer: Analyzer, builder: Builder):
        self.analyzer = analyzer
        self.builder = builder


class Language():
    def __init__(self):
        self.filetypes: list[str] = []
        self.frameworks: list[Framework]

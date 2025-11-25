from src.analyzer import Analyzer
from src.builder import Builder


class Framework():
    def __init__(self, analyzer: Analyzer, builder: Builder):
        self.analyzer = analyzer
        self.builder = builder

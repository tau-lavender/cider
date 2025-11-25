from pathlib import Path
from enum import Enum


class Analyzer():
    def __init__(self):
        pass

    def analyze(self, files: str):
        pass


class MainAnalyzer():
    """
    Главный аналайзер. Загружает другие аналайзеры и дайт им файлы.
    """

    def __init__(self, path: Path):
        self.path = path
        self.analyzers: list[Analyzer] = []

    def load_analyzers(self):
        pass

    def analyze(self):
        """
        Ходим по файлам, кидаем их в аналайзеры
        """
        for root, dirs, files in self.path.walk():
            for analyzer in self.analyzers:
                analyzer.analyze(files)

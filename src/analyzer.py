from pathlib import Path
from enum import Enum

from src.language import Language


class MainAnalyzer():
    """
    Главный аналайзер. Загружает другие аналайзеры и дайт им файлы.
    """

    def __init__(self, path: Path):
        self.path = path
        self.languages: list[Language] = []

    def load_analyzers(self):
        pass

    def analyze(self):
        print("!!!!")
        """
        Ходим по файлам, кидаем их в аналайзеры
        """
        for root, dirs, files in self.path.walk():
            for language in self.languages:
                # TODO
                # re.mask(files, language.masks)
                pass

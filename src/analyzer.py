from pathlib import Path
from enum import Enum

import importlib
import inspect

from src.language import Language
from src.configs.language import LANGUAGES_IMPORT_CONFIG


class MainAnalyzer():
    """
    Главный аналайзер. Загружает другие аналайзеры и дайт им файлы.
    """

    def __init__(self, path: Path):
        self.path = path
        self.languages: list[Language] = []

    def load_languages(self):
        for plugin_name in LANGUAGES_IMPORT_CONFIG:
            mod = importlib.import_module(plugin_name)
            classes = inspect.getmembers(mod, inspect.isclass)
            for language in classes:
                if isinstance(language, Language):
                    self.languages.append(language)

    def analyze(self):
        """
        Ходим по файлам, кидаем их в аналайзеры
        """
        for root, dirs, files in self.path.walk():
            for language in self.languages:
                # TODO
                # re.mask(files, language.masks)
                pass

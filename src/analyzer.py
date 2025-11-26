import os

from pathlib import Path
from enum import Enum

import fnmatch

import importlib
import inspect

from src.default_class import Language
from src.configs.language import LANGUAGES_IMPORT_CONFIG


class MainAnalyzer():
    """
    Главный аналайзер. Загружает другие аналайзеры и дайт им файлы.
    """

    def __init__(self):
        self.language_found = None
        self.languages: list[Language] = []

    def load_languages(self):
        for plugin_name in LANGUAGES_IMPORT_CONFIG:
            mod = importlib.import_module(plugin_name)
            classes = inspect.getmembers(mod, inspect.isclass)
            for language in classes:
                if not issubclass(Language, language[1]) and issubclass(language[1], Language):
                    language_instance = language[1]()
                    language_instance.load_frameworks()
                    self.languages.append(language_instance)

    def analyze(self):
        """
        Ходим по файлам, кидаем их в аналайзеры
        """
        for root, dirs, files in Path(os.getcwd()).walk():
            for file in files:
                if self.language_found is not None: # TODO поддержка мультиязычности
                    for mask in self.language_found.masks:
                        if fnmatch.fnmatch(file, mask) or file == mask:
                            self.language_found.analyze(root / file)
                            break
                else:
                    for language in self.languages: # TODO: объединить
                        for mask in language.masks:
                            if fnmatch.fnmatch(file, mask) or file == mask:
                                language.analyze(root / file)
                                self.language_found = language
                                print(f"* Detected language: {language.name}")
                                break
    
    def build(self):
        if self.language_found is None:
            raise RuntimeError("No language found")
        self.language_found.build()

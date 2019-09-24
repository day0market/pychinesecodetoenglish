import logging
import os
import time
from typing import List

from googletrans import Translator


class AbstractTranslator:

    def __init__(self, path: str, translate_strings: bool = True, language: str = 'en', encoding: str = "utf8"):
        self.__content = self._read_file(path, encoding)
        self.__do_strings = translate_strings
        self.__lang = language.lower()

    @property
    def do_strings(self) -> bool:
        return self.__do_strings

    @property
    def lang(self) -> str:
        return self.__lang

    @property
    def content(self) -> str:
        return self.__content

    @staticmethod
    def _read_file(path, encoding):
        with open(path, 'r', encoding=encoding) as f:
            data = f.read()
        return data

    def translate_str(self, original: str) -> str:
        raise NotImplementedError()

    def get_result(self) -> str:
        raise NotImplementedError()


class GoogleTranslator(AbstractTranslator):

    def __init__(self, path: str, translate_strings: bool = True, language: str = 'en', encoding: str = "utf8"):
        super().__init__(path, translate_strings, language, encoding)
        self._translator = Translator(service_urls=self._get_google_urls())

    @staticmethod
    def _get_google_urls() -> List[str]:
        pth = os.path.join(os.path.dirname(__file__), 'domains.txt')
        with open(pth) as f:
            domains = f.read().splitlines()

        return domains

    def translate_str(self, original: str) -> str:
        tries = 0
        while tries < 15:
            try:
                return self._translator.translate(original, self.lang).text
            except Exception as e:
                logging.error(f'Tries: {tries}. Exception: {e}')
                tries += 1
                time.sleep(60 * 5)

    def get_result(self) -> str:
        raise NotImplementedError()

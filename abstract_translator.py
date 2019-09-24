import logging
import os
import re
import time
from typing import List

from googletrans import Translator


class AbstractTranslator:

    def __init__(self, path: str, language: str = 'en', encoding: str = "utf8"):
        self.__content = self._read_file(path, encoding)
        self.__lang = language.lower()

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

    def get_provider_answer(self, original: str) -> str:
        raise NotImplementedError()

    def get_result(self) -> str:
        raise NotImplementedError()


class GoogleTranslator(AbstractTranslator):
    """
    Free translation by Google translate with package `googletrans`
    """

    def __init__(self, path: str, language: str = 'en', encoding: str = "utf8"):
        super().__init__(path, language, encoding)
        self._translator = Translator(service_urls=self._get_google_urls())

    @staticmethod
    def _get_google_urls() -> List[str]:
        pth = os.path.join(os.path.dirname(__file__), 'domains.txt')
        with open(pth) as f:
            domains = f.read().splitlines()

        return domains

    def get_provider_answer(self, original: str) -> str:
        tries = 0
        while tries < 15:
            try:
                return self._translator.translate(original, self.lang).text
            except Exception as e:
                logging.error(f'Tries: {tries}. Exception: {e}')
                tries += 1
                time.sleep(60 * 5)

    def translate(self, original: str) -> str:
        raise NotImplementedError()

    def get_result(self):
        res = re.sub(u'[\u4e00-\u9fff]+', lambda x: self.translate(x.group()), self.content)
        return res

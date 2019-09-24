import re
import time

from abstract_translator import GoogleTranslator


class MarkdownTranslator(GoogleTranslator):

    def get_result(self) -> str:
        if len(self.content) > 2000:
            return self._do_chunks()

        return self._translate(self.content)

    def _translate(self, original: str) -> str:
        translated = self.translate_str(original)
        time.sleep(0.5)
        return self.fix_uppercase(translated)

    def _do_chunks(self) -> str:
        text_left = self.content
        ready = ''
        while True:
            time.sleep(0.5)
            if len(text_left) < 2000:
                ready += self._translate(text_left)
                break

            buffer = text_left[:1800]

            # Loop util nearest dot. Than translate and cut text
            for i, c in enumerate(text_left[1800:2000]):
                buffer += c
                if c == '.':
                    text_left = text_left[1800 + i:]
                    break

            ready += self._translate(buffer)

        return ready

    @staticmethod
    def fix_uppercase(translated: str) -> str:
        translated = translated[0].lower() + translated[1:]
        return re.sub(r'\s{2,}\b\w', lambda x: x.group().lower(), translated)

import time

from abstract_translator import GoogleTranslator


class MarkdownTranslator(GoogleTranslator):
    symbols_in_request = 2000

    def translate(self, original: str) -> str:
        if len(original) > self.symbols_in_request:
            return self._do_chunks(original)

        translated = self.get_provider_answer(original)
        time.sleep(0.5)
        return f" {translated.lower()} "

    def _do_chunks(self, original) -> str:
        text_left = original
        ready = ''
        while True:
            time.sleep(0.5)
            if len(text_left) < self.symbols_in_request:
                ready += f' {self.get_provider_answer(text_left).lower()} '
                break

            buffer = text_left[:self.symbols_in_request-200]

            # Loop util nearest dot. Than translate and cut text
            for i, c in enumerate(text_left[self.symbols_in_request-200:self.symbols_in_request]):
                buffer += c
                if c == '.':
                    text_left = text_left[self.symbols_in_request-200 + i:]
                    break

            ready += self.get_provider_answer(buffer)

        return ready

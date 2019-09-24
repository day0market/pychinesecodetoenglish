from abstract_translator import GoogleTranslator


class PyFileTranslator(GoogleTranslator):

    @staticmethod
    def _is_empty_match(data):
        chars = set(data)
        diff = chars - {'"', "'"}
        return len(diff) == 0

    def translate(self, original):
        if not original or self._is_empty_match(original):
            return original

        translated = self.get_provider_answer(original)
        return f' {translated.lower()} '

import re

from abstract_translator import GoogleTranslator


class PyFileTranslator(GoogleTranslator):

    @staticmethod
    def _is_empty_match(data):
        chars = set(data)
        diff = chars - {'"', "'"}
        return len(diff) == 0

    def _translate(self, original):
        if not original or self._is_empty_match(original):
            return original

        translated = self.translate_str(original)
        translated = self.fix_uppercase_in_format_strings(original, translated)
        return f' {translated.lower()} '

    @staticmethod
    def fix_uppercase_in_format_strings(original, translated):
        if '{' not in original:
            return translated

        template_names = re.findall('{\w*}', original)  # all template usages

        for t in template_names:
            t_upper = t[0] + t[1].upper() + t[2:]  # make title case
            translated = translated.replace(t_upper, t)

        return translated

    def get_result(self):
        res = re.sub(u'[\u4e00-\u9fff]+', lambda x: self._translate(x.group()), self.content)
        #res = re.sub(r"'''(\s*|.*)*'''", lambda x: self._translate(x.group()), res)
        #res = re.sub(r"'(.*|\s*)'", lambda x: self._translate(x.group()), res)
        #res = re.sub(r'"(.*|\s*)"', lambda x: self._translate(x.group()), res)
        #res = re.sub(r'#.+', lambda x: self._translate(x.group()), res)
        return res

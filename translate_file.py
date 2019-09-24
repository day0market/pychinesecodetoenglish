class BaseFileTranslator:

    def __init__(self, path, translate_strings=True, language='EN'):
        self._content = self._read_file(path)
        self._do_strings = translate_strings
        self._lang = language

    @staticmethod
    def _read_file(path):
        with open(path, 'r', encoding="utf8") as f:
            data = f.read()
        return data

    def get_result(self):

        is_multiline_comment = False
        buffer = []
        translated = ''
        for r in self._content.splitlines():

            if is_multiline_comment:
                # we have open multi line comment. put things in buffer until we get closing tag
                finished_multi = self._multiline_finished(r)
                buffer.append(r)

                if finished_multi:
                    translated += f'{self._translate_buffer(buffer)}\n'
                    buffer = []
                    is_multiline_comment = False
                continue

            multiline_started = self._multiline_started(r)

            if multiline_started:
                is_multiline_comment = True
                buffer.append(r)
                continue

            line_is_comment = self._line_starts_with_sharp(r)

            # this line is comment. Just add it to buffer and continue. Fill buffer until we get code row
            if line_is_comment:
                buffer.append(r)
                continue

            # this line is not comment. but maybe we have comments in buffer?
            if buffer:
                translated += f'{self._translate_buffer(buffer)}\n'
                buffer = []

            translated += f'{self._translate_code_line(r)}\n'

        return translated

    def _translate_code_line(self, code_row):
        comment_tag = ('"', "'")
        string_buffer = ''
        string_open = ''
        translated = ''
        for i, letter in enumerate(code_row):
            if letter in comment_tag:
                if string_open:  # so this is closing string tag
                    if self._do_strings:
                        translated_str = self.translate(string_buffer)
                    else:
                        translated_str = string_buffer
                    string_buffer = ''
                    translated += translated_str + letter
                    string_open = False
                else:
                    # this is opening string tag
                    translated += letter
                    string_buffer = ''
                    string_open = True
            else:
                if string_open:
                    string_buffer += letter
                else:
                    if letter == '#':  # inline comment strating point. Translate all until end ot the line
                        translated_comment = self.translate(code_row[i:])
                        translated += translated_comment
                        break
                    translated += letter

        assert not string_open
        assert not string_buffer

        return translated

    @staticmethod
    def _multiline_started(code_line):
        start_index = 0
        for i, c in enumerate(code_line):
            if c == ' ':
                continue
            start_index = i
            break

        if len(code_line) < start_index + 3:
            return False

        first_3_symbols = code_line[start_index:start_index + 3]
        return first_3_symbols == "'''" or first_3_symbols == '"""'

    @staticmethod
    def _line_starts_with_sharp(code_line):
        for c in code_line:
            if c == ' ':
                continue
            return c == '#'

    @staticmethod
    def _multiline_finished(row):
        return row.endswith("'''") or row.endswith('"""')

    def _translate_buffer(self, buffer):
        str_repr = '\n'.join(buffer)
        return self.translate(str_repr)

    def translate(self, row):
        return row

import os

from markdown_translator import MarkdownTranslator
from pyfile_translator import PyFileTranslator


def test_fix_uppercase():
    original = 'f"{field_name}参数类型应为{field_type}，请检查！"'
    translated = 'f"{Field_name} parameter type should {field_type}, check!"'

    fixed = PyFileTranslator.fix_uppercase_in_format_strings(original, translated)

    assert fixed == 'f"{field_name} parameter type should {field_type}, check!"', fixed


def test_file_translator():
    filepath = os.path.join(os.path.dirname(__file__), 'data', 'widget.py')
    translator = PyFileTranslator(filepath)
    with open(filepath, 'r', encoding="utf8") as f:
        orginal = f.read().splitlines()

    translated = translator.get_result()

    with open('generated.py', 'w', encoding="utf8") as f:
        f.write(translated)

    translated_list = translated.splitlines()
    assert len(translated_list) == len(orginal)


def test_markdown_translator_fix_uppercase():
    filepath = os.path.join(os.path.dirname(__file__), 'data', 'sample.md')
    with open(filepath, 'r', encoding="utf8") as f:
        test_text = f.read()

    result = MarkdownTranslator.fix_uppercase(test_text)

    assert result != test_text
    for row in result.splitlines():
        if not row:
            continue
        for letter in row:
            if letter in ('#', '-'):
                break
            if letter.isalpha():
                assert letter.islower(), print(letter)
                break


if __name__ == '__main__':
    test_file_translator()
    test_markdown_translator_fix_uppercase()
    test_fix_uppercase()


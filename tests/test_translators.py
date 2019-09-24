import os

from pyfile_translator import PyFileTranslator


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


if __name__ == '__main__':
    test_file_translator()

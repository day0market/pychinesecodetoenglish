import argparse
import logging
import os
import shutil

from markdown_translator import MarkdownTranslator
from pyfile_translator import PyFileTranslator


def ignore_folder(folder) -> bool:
    if '__pycache__' in folder or '.git' in folder:
        return True
    return False


def translate_file(base_dir, rel_path, save_dir, file_name):
    logging.info(f'Translating: {rel_path} {file_name}')
    if file_name.endswith('.md'):
        tr = MarkdownTranslator(os.path.join(base_dir, rel_path, file_name))
    elif file_name.endswith('.py'):
        tr = PyFileTranslator(os.path.join(base_dir, rel_path, file_name))
    else:
        raise Exception(f'Not expected extension {file_name}')

    res = tr.get_result()
    save_path = os.path.join(save_dir, rel_path, file_name) if rel_path != '.' else os.path.join(save_dir, file_name)

    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(res)

    logging.info(f'Done: {file_name}')


def run(base_dir, save_dir, force=False):
    extensions = {'md'}
    for dir_name, _, files in os.walk(base_dir):
        if ignore_folder(dir_name):
            continue

        rel_path = os.path.relpath(dir_name, base_dir)

        if not os.path.exists(os.path.join(save_dir, rel_path)):  # make subdir if not exists
            os.mkdir(os.path.join(save_dir, rel_path))

        for f in files:
            exists = os.path.exists(os.path.join(save_dir, rel_path, f))

            if f.split('.')[-1] in extensions and (not exists or force):
                translate_file(base_dir, rel_path, save_dir, f)
                continue

            if not exists:
                shutil.copy(os.path.join(dir_name, f), os.path.join(save_dir, rel_path, f))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Translate chinese code to english', add_help=True)
    parser.add_argument('source_path', type=str, help='path to package you want to translate')
    parser.add_argument('destination_path', type=str, help='path where you want to put translated file')
    parser.add_argument('--level', help='logging level', default='WARNING')
    parser.add_argument('--force', help='force re translate if file already exists', default=False, action='store_true')

    args = parser.parse_args()
    logging.basicConfig(level=args.level)
    run(args.source_path, args.destination_path, force=args.force)

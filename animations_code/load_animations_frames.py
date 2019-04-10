from os import path, listdir
from collections import OrderedDict


def read_file_content(folder_path: str, filename: str):
    with open(path.join(folder_path, filename)) as r:
        return r.read()


def list_files_in_folder(folder_path):
    if not path.isdir(folder_path):
        raise IOError(f'Folder "{folder_path}" is missing.')

    return [
        file
        for file in listdir(folder_path)
        if path.isfile(path.join(folder_path, file))
    ]


def load_animations_from_folder(folder_path: str) -> OrderedDict:
    animations = {}
    files = list_files_in_folder(folder_path)
    for filename in files:
        file_content = read_file_content(folder_path, filename)
        animations[filename] = file_content

    return OrderedDict(sorted(animations.items()))

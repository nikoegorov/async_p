from os import path, listdir


def read_file_contents(folder_path: str, filename: str) -> tuple:
    with open(path.join(folder_path, filename)) as r:
        return (filename, r.read())


def list_files_in_folder(folder_path):
    if not path.isdir(folder_path):
        raise IOError(f'Folder "{folder_path}" is missing.')

    return [
        file
        for file in listdir(folder_path)
        if path.isfile(path.join(folder_path, file))
    ]


def load_animations_from_folder(folder_path: str):
    animations = []
    files = list_files_in_folder(folder_path)
    for filename in files:
        animation_in_file = read_file_contents(folder_path, filename)
        animations.append(animation_in_file)

    return sorted(animations)

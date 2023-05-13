# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

import os


def walk_files(path):
    files = []

    for root, dirs, files_in_dir in os.walk(path):
        for filename in files_in_dir:
            files.append(os.path.join(root, filename))

    return files

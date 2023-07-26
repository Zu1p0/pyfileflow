from pathlib import Path
from .types import SUPPORTED_PATHS_TYPES, PATH_LIST_TYPE
from typing import Sequence, TypeGuard

def path_parameter_to_path_list(path: SUPPORTED_PATHS_TYPES) -> PATH_LIST_TYPE:
    if path is None:
        return []

    path_list: PATH_LIST_TYPE = []
    if not (isinstance(path, Sequence) and not isinstance(path, str)):
        path = [path]

    for unique_path in path:
        if isinstance(unique_path, str):
            unique_path = Path(unique_path)
        if not isinstance(unique_path, Path):
            raise TypeError("Invalid path format")
        unique_path: TypeGuard[Path]

        path_list.append(unique_path)

    return path_list


def clear_directory(path: Path):
    for item in path.iterdir():
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            item.rmdir()
    return 0

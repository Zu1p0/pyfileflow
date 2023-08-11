import os
from pathlib import Path

from typing_extensions import Self, Union

from .types import PathLike


class FSElement:
    def __init__(self: Self, path: PathLike) -> None:
        self.path = Path(path)

        if not self.path.exists():
            raise FileNotFoundError

    @property
    def name(self: Self) -> str:
        return self.path.name

    @property
    def size(self: Self) -> int:
        return self.path.stat().st_size


class File(FSElement):
    def __init__(self: Self, path: PathLike, *args, **kwargs) -> None:
        super().__init__(path, *args, **kwargs)

        if not self.path.is_file():
            raise IsADirectoryError

    @property
    def extension(self: Self) -> str:
        return self.path.suffix


class Folder(FSElement):
    def __init__(self: Self, path: PathLike, *args, **kwargs) -> None:
        super().__init__(path, *args, **kwargs)

        if not self.path.is_dir():
            raise NotADirectoryError

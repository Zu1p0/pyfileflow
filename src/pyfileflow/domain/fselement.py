from pathlib import PurePath
from typing import Union
import os


class FSElement:
    def __init__(self, path: Union[PurePath, str, os.PathLike]) -> None:
        self.path = PurePath(path)

    def is_folder(self) -> bool:
        if self.path.suffix == "":
            return True
        else:
            return False

    @property
    def name(self) -> str:
        return self.path.name

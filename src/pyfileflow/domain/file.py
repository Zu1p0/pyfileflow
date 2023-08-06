from pathlib import PurePath

from typing import Union

from .exceptions import InvalidFilePath
from .fselement import FSElement


class File(FSElement):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.is_folder():
            raise InvalidFilePath

    @property
    def extension(self) -> str:
        return self.path.suffix

from pathlib import PurePath

from .exceptions import InvalidFolderPath
from .fselement import FSElement


class Folder(FSElement):
    def __init__(self, path: PurePath):
        super().__init__(path)

        if not self.is_folder():
            raise InvalidFolderPath

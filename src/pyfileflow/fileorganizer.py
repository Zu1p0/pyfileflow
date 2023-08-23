from types import TracebackType

from typing_extensions import Optional, Self, Union

from . import utils
from .path import PathLike, PPath


class FileOrganizer(object):
    def __init__(
        self,
        folder: Optional[Union[PathLike, list[PathLike]]] = None,
    ) -> None:
        self.folder: list[PPath] = [PPath(path) for path in utils.parse_args(folder)]

        if not all([path.exists() for path in self.folder]):
            raise FileNotFoundError("All paths to sort must exists")

        if not all([path.is_dir() for path in self.folder]):
            raise NotADirectoryError("All paths to sort must be directories")

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        t: Union[type[BaseException], None],
        v: Union[BaseException, None],
        tb: Union[TracebackType, None],
    ) -> None:
        pass

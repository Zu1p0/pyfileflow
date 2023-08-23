import os
import pathlib
import shutil
from types import TracebackType

from typing_extensions import Self, Union


class PPath(pathlib.Path):
    _flavour = type(pathlib.Path())._flavour

    def delete(self) -> None:
        if self.is_dir():
            shutil.rmtree(self)
        else:
            self.unlink()

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        t: Union[type[BaseException], None],
        v: Union[BaseException, None],
        tb: Union[TracebackType, None],
    ) -> None:
        pass


PathLike = Union[PPath, pathlib.Path, str, os.PathLike]

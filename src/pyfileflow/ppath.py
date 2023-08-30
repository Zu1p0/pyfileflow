"""Path interface.

Implement a subclass of pathlib.Path called PPath.
"""

import os
import pathlib
import shutil
from types import TracebackType

from typing_extensions import Optional, Self, Union


class PPath(pathlib.Path):
    """Custom Path class that extends pathlib.Path with additional methods."""

    _flavour = type(pathlib.Path())._flavour

    def delete(self, missing_ok: bool=False) -> None:
        """Delete the path in the filesystem.

        Deletes a directory and its contents or a file depending on the path type.

        Args:
            missing_ok (bool): If True, do not raise an exception if the path does not exist.
                Defaults to False.

        Raises:
            FileNotFoundError: If the path does not exist and `missing_ok` is False.
            OSError: If there are permission issues or other errors during deletion.
        """
        if self.exists() or not missing_ok:
            if self.is_dir():
                shutil.rmtree(self)
            else:
                self.unlink()

    def __enter__(self) -> Self:
        """Enter a context manager.

        Returns:
            PPath: The current PPath instance.
        """
        return self

    def __exit__(
        self,
        t: Optional[type[BaseException]],
        v: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        """Exit a context manager.

        Args:
            t (Optional[type[BaseException]]): Type of the exception raised, if any.
            v (Optional[BaseException]): The exception instance, if raised.
            tb (Optional[TracebackType]): Traceback information.
        """


PathLike = Union[PPath, pathlib.Path, str, os.PathLike]

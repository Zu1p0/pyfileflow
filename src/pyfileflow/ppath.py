"""Path interface.

Implement a subclass of pathlib.Path called PPath.
"""

import os
import pathlib
import shutil
from types import TracebackType

from typing_extensions import Optional, Self, Union


class PPath(pathlib.Path):
    """Custom Path class that extends pathlib.Path with additional functionalities.

    Attributes:
        extension (str): The path extension.
    """

    _flavour = type(pathlib.Path())._flavour

    _planned_delete: bool = False

    def delete(self, missing_ok: bool = False) -> None:
        """Delete the path in the filesystem.

        Deletes a directory and its contents or a file depending on the path type.

        Args:
            missing_ok (bool):
                If True, do not raise an exception if the path does not exist.
                Defaults to False.
        """
        if self.exists() or not missing_ok:
            if self.is_dir():
                shutil.rmtree(self)
            else:
                self.unlink()

    def plan_delete(self) -> None:
        """Plan the deletion of the file.

        This method sets an internal flag to indicate that the file should be deleted
        during the appropriate process, usually after certain rules have been applied.
        """
        self._planned_delete = True

    def delete_if_planned(self) -> None:
        """Delete the file if planned for deletion.

        This method checks if the file has been planned for deletion using the
        `plan_delete` method. If it has been planned for deletion, the file is deleted.
        """
        if self._planned_delete:
            self.delete()

    @property
    def extension(self) -> str:
        """The path extension.

        Considering that Path.suffix only returns the last extension, and that
        Path.suffixes returns a list of extensions, PPath.extension is needed
        to return a string of all extensions.

        Returns:
            str: The path extension.
        """
        return "".join(self.suffixes)

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

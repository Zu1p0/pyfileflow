"""Test module for pyfileflow.ppath module.

This module contains unit tests for the PPath class and its related functionality.
"""

import pathlib

import pytest
from pyfakefs.fake_filesystem import FakeFilesystem

from pyfileflow.ppath import PPath


def test_path_instancing() -> None:
    """Test PPath instance creation.

    This test checks the creation of a PPath instance and its type
    compatibility with both PPath and pathlib.Path classes.
    """
    path = PPath("")

    assert path
    assert isinstance(path, PPath)
    assert isinstance(path, pathlib.Path)


def test_context_manager() -> None:
    """Test PPath instance usage within a context manager.

    This test checks the behavior of a PPath instance within a context manager
    and verifies its type compatibility with both PPath and pathlib.Path
    classes.
    """
    with PPath("folder") as path:
        assert path
        assert isinstance(path, PPath)
        assert isinstance(path, pathlib.Path)


def test_del_file(fs: FakeFilesystem) -> None:
    """Test file deletion using PPath instance.

    This test verifies the deletion of a file using a PPath instance.
    It creates a file using pyfakefs and then deletes it using the PPath
    instance. The assertions ensure that the file is initially present and then
    properly deleted.
    """
    file_path = PPath("file")
    file_path.touch()

    assert file_path.exists()
    assert file_path.is_file()

    file_path.delete()

    assert not file_path.exists()


def test_del_folder(fs: FakeFilesystem) -> None:
    """Test folder deletion using PPath instance.

    This test verifies the deletion of a folder using a PPath instance. It
    creates a folder using pyfakefs and then deletes it using the PPath
    instance. The assertions ensure that the folder is initially present and
    then properly deleted.
    """
    folder_path = PPath("folder")
    folder_path.mkdir()

    assert folder_path.exists()
    assert folder_path.is_dir()

    folder_path.delete()

    assert not folder_path.exists()


def test_del_missing_ok(fs: FakeFilesystem) -> None:
    """Test the missing_ok argument of PPath.delete()."""
    not_exist_path = PPath("/test/")

    assert not not_exist_path.exists()

    with pytest.raises(FileNotFoundError):
        not_exist_path.delete()

    not_exist_path.delete(missing_ok=True)

    assert not not_exist_path.exists()


def test_extension() -> None:
    """Test the extension argument of PPath."""
    assert PPath("file.txt").extension == ".txt"
    assert PPath("file.tar.gz").extension == ".tar.gz"

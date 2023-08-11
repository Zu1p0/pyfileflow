from pathlib import Path

import pytest
from pyfakefs.fake_filesystem import FakeFilesystem

from pyfileflow.fselements import File, Folder, FSElement


# Tests FSElement
def test_fselement_creation(fs: FakeFilesystem) -> None:
    file_path = Path("test.txt")
    file_path.touch()

    fselement = FSElement(file_path)

    assert fselement
    assert fselement.name == "test.txt"
    assert fselement.size == file_path.stat().st_size


def test_fselement_FileNotFoundError(fs: FakeFilesystem) -> None:
    with pytest.raises(FileNotFoundError):
        FSElement("test.txt")


# Tests File
def test_file_creation(fs: FakeFilesystem) -> None:
    file_path = Path("test.txt")
    file_path.touch()

    file = File(file_path)

    assert file
    assert file.name == "test.txt"
    assert file.size == 0
    assert file.extension == ".txt"


def test_file_IsADirectoryError(fs: FakeFilesystem) -> None:
    with pytest.raises(IsADirectoryError):
        File("/")


# Tests Folder
def test_folder_creation(fs: FakeFilesystem) -> None:
    folder_path = Path("/test_path/")
    folder_path.mkdir()

    folder = Folder(folder_path)

    assert folder
    assert folder.name == "test_path"
    assert folder.size == 0


def test_folder_NotADirectoryError(fs: FakeFilesystem) -> None:
    file_path = Path("/test.txt")
    file_path.touch()
    with pytest.raises(NotADirectoryError):
        Folder(file_path)

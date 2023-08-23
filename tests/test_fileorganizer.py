import pytest

from pyfileflow.fileorganizer import FileOrganizer
from pyfileflow.path import PPath

from pyfakefs.fake_filesystem import FakeFilesystem



def test_file_organizer_instancing() -> None:
    organizer = FileOrganizer(folder="/")

    assert organizer
    assert all([isinstance(path, PPath) for path in organizer.folder])
    assert organizer.folder == [PPath("/")]


def test_file_organizer_context_manager() -> None:
    with FileOrganizer(folder="/") as organizer:
        assert organizer


def test_file_organizer_raises_not_found(fs: FakeFilesystem) -> None:
    with pytest.raises(FileNotFoundError):
        FileOrganizer(folder=["/", "/this_does_not_exist"])


def test_file_organizer_raises_not_a_directory(fs: FakeFilesystem) -> None:
    file = PPath("test.txt")
    file.touch()

    with pytest.raises(NotADirectoryError):
        FileOrganizer(folder=["/", "test.txt"])

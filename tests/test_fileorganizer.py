import pytest
from pyfakefs.fake_filesystem import FakeFilesystem

from pyfileflow.fileorganizer import FileOrganizer
from pyfileflow.path import PPath
from pyfileflow.rule import Rule


def test_file_organizer_instancing() -> None:
    organizer = FileOrganizer(folder="/", rule=Rule())

    assert organizer
    assert organizer.folder == [PPath("/")]
    assert organizer.rule == [Rule()]


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

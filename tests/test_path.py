import pathlib

from pyfakefs.fake_filesystem import FakeFilesystem

from pyfileflow.path import PPath


def test_path_instancing() -> None:
    path = PPath("")

    assert path
    assert isinstance(path, PPath)
    assert isinstance(path, pathlib.Path)


def test_context_manager() -> None:
    with PPath("folder") as path:
        assert path
        assert isinstance(path, PPath)
        assert isinstance(path, pathlib.Path)


def test_del_file(fs: FakeFilesystem) -> None:
    file_path = PPath("file")
    file_path.touch()

    assert file_path.exists()
    assert file_path.is_file()

    file_path.delete()

    assert not file_path.exists()


def test_del_folder(fs: FakeFilesystem) -> None:
    folder_path = PPath("folder")
    folder_path.mkdir()

    assert folder_path.exists()
    assert folder_path.is_dir()

    folder_path.delete()

    assert not folder_path.exists()

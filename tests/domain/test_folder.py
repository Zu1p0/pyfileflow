import pathlib

import pydantic
import pytest

from pyfileflow.domain.folder import Folder

def test_folder_create():
    folder = Folder(path="parent/folder")

    assert folder
    assert folder.path == pathlib.PurePath("parent/folder")
    assert folder.name == "folder"

def test_error_throw_when_not_folder():
    with pytest.raises(pydantic.ValidationError):
        Folder(path="parent/folder/file.txt")
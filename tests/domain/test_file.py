import pathlib

import pydantic
import pytest

from pyfileflow.domain.file import File
from pyfileflow.domain.exceptions import 


def test_file_create():
    file = File(path="folder/subfolder/file.txt")

    assert file
    assert file.path == pathlib.PurePath("folder/subfolder/file.txt")
    assert file.name == "file.txt"
    assert file.extension == ".txt"


def test_error_throw_when_not_file():
    with pytest.raises(pydantic.ValidationError):
        File(path="folder/subfolder/")

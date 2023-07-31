import shutil

import pytest
from conftest import PARENT_PATH

import pyfileflow.utils.utils as utils


@pytest.fixture
def fake_filesystem(fs):
    yield fs


def test_clear_directory():
    temp_test_folder_path = PARENT_PATH / "temp_test_clear_folder"
    temp_test_folder_path.mkdir(exist_ok=True)

    try:
        for index in range(2):
            temp_test_PARENT_PATH = (
                temp_test_folder_path / "temp_test_file_{}.txt".format(index)
            )
            temp_test_dir_path = temp_test_folder_path / "temp_test_dir_{}".format(
                index
            )
            temp_test_PARENT_PATH.touch(exist_ok=True)
            temp_test_dir_path.mkdir(exist_ok=True)

        utils.clear_directory(temp_test_folder_path)

        assert not any(temp_test_folder_path.iterdir())

    finally:
        shutil.rmtree(temp_test_folder_path)

import shutil

import pytest
from conftest import FILE_PATH

import pyfileflow.utils.utils as utils


@pytest.mark.e2e
def test_clear_directory():
    temp_test_folder_path = FILE_PATH / "temp_test_clear_folder"
    temp_test_folder_path.mkdir(exist_ok=True)

    try:
        for index in range(2):
            temp_test_file_path = (
                temp_test_folder_path / "temp_test_file_{}.txt".format(index)
            )
            temp_test_dir_path = temp_test_folder_path / "temp_test_dir_{}".format(
                index
            )
            temp_test_file_path.touch(exist_ok=True)
            temp_test_dir_path.mkdir(exist_ok=True)

        utils.clear_directory(temp_test_folder_path)

        assert not any(temp_test_folder_path.iterdir())

    finally:
        shutil.rmtree(temp_test_folder_path)

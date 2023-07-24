import pyfileflow as pff
import pyfileflow.utils as utils
import pytest
import pathlib
import shutil


FILE_PATH = pathlib.Path(__file__).resolve().parent


@pytest.fixture
def file_organizer_test_instance():
    return pff.FileOrganizer()


def test_file_organizer_test_instance(file_organizer_test_instance):
    assert isinstance(file_organizer_test_instance, pff.FileOrganizer)


def test_get_add_directory(file_organizer_test_instance):
    for test_path in [
        FILE_PATH,
        str(FILE_PATH),
        (FILE_PATH),
        [FILE_PATH],
        [str(FILE_PATH)],
    ]:
        try:
            file_organizer_test_instance.add_directory(test_path)
            assert FILE_PATH in file_organizer_test_instance.get_directories()
        finally:
            file_organizer_test_instance.empty_directories()


@pytest.mark.e2e
def test_clear_directory():
    temp_test_folder_path = FILE_PATH / "temp_test_clear_folder"
    temp_test_folder_path.mkdir(exist_ok=False)

    try:
        for index in range(5):
            temp_test_file_path = temp_test_folder_path / "temp_test_file{}.txt".format(
                index
            )
            temp_test_file_path.touch()

        utils.clear_directory(temp_test_folder_path)

        assert not any(temp_test_folder_path.iterdir())

    finally:
        shutil.rmtree(temp_test_folder_path)

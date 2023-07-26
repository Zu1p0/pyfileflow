import pathlib

import pytest

import pyfileflow as pff

FILE_PATH = pathlib.Path(__file__).resolve().parent


@pytest.fixture
def file_organizer_test_instance():
    return pff.FileOrganizer()


def test_get_add_monitoring_directory(file_organizer_test_instance: pff.FileOrganizer):
    try:
        for test_path in [
            FILE_PATH,
            str(FILE_PATH),
            (FILE_PATH),
            [FILE_PATH],
            [str(FILE_PATH)],
        ]:
            file_organizer_test_instance.set_directory_to_monitor(test_path)
            assert FILE_PATH in file_organizer_test_instance.get_monitored_directory()
    finally:
        file_organizer_test_instance.empty_directory()



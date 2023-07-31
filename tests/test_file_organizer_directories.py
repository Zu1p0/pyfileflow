import pathlib

import pytest

import pyfileflow as pff

fake_test_path = "this/is/a/fake/path"

@pytest.fixture
def file_organizer_test_instance():
    return pff.FileOrganizer()


def test_get_add_monitoring_directory(file_organizer_test_instance):
    try:
        for test_path in [
            fake_test_path,
            str(fake_test_path),
            (fake_test_path),
            [fake_test_path],
            [str(fake_test_path)],
        ]:
            file_organizer_test_instance.set_directory_to_monitor(test_path)
            assert fake_test_path in file_organizer_test_instance.get_monitored_directory()
    finally:
        file_organizer_test_instance.empty_directory()

def test_add_monitored_directory(file_organizer_test_instance):

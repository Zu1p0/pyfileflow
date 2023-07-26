import pytest
import pathlib

def pytest_configure(config):
    config.addinivalue_line("markers", "e2e: mark as end-to-end test.")

FILE_PATH = pathlib.Path(__file__).resolve().parent

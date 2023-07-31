from typing import NoReturn

from .utils.alias import alias_method, alias_class
from .utils.utils import path_parameter_to_path_list
from .utils.types import SupportedPathTypes, PathListType

@alias_class
class FileOrganizer:
    directories: PathListType = []

    def __init__(self):
        pass

    @alias_method("add_directory", "add_directories", "add_directories_to_monitor")
    def add_directory_to_monitor(self, path: SupportedPathTypes) -> NoReturn:
        self.directories += path_parameter_to_path_list(path)

    @alias_method("set_directories_to_monitor", "set_directories", "set_directory")
    def set_directory_to_monitor(self, path: SupportedPathTypes) -> NoReturn:
        self.directories = path_parameter_to_path_list(path)

    @alias_method("get_directories", "get_directory", "get_monitored_directories")
    def get_monitored_directory(self) -> PathListType:
        return self.directories

    @alias_method("empty_directories")
    def empty_directory(self) -> NoReturn:
        self.directories = []

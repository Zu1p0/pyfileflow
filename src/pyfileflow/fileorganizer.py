from typing import Optional, Union, List, TypeGuard, Sequence, NoReturn
from pathlib import Path


class FileOrganizer:
    directories: List[Path] = []

    def __init__(self):
        self.add_directory = self.add_directory_to_monitor
        self.get_directories = self.get_monitored_directories

    def add_directory_to_monitor(
        self, path: Optional[Union[str, Path, Sequence[Union[str, Path]]]]
    ) -> NoReturn:
        if path is not None:
            if not (isinstance(path, Sequence) and not isinstance(path, str)):
                path = [path]

            for unique_path in path:
                if isinstance(unique_path, str):
                    unique_path = Path(unique_path)
                if not isinstance(unique_path, Path):
                    raise TypeError("Invalid path format")
                unique_path: TypeGuard[Path]

                self.directories.append(unique_path)

    def get_monitored_directories(self) -> List[Path]:
        return self.directories

    def empty_directories(self) -> NoReturn:
        self.directories = []

from pathlib import Path

from fselements import File, Folder, FSElement
from typing_extensions import Callable, List, Optional, Self, TypeAlias, Union

from .types import PathLike, RuleCondition


class Rule:
    def __init__(
        self: Self,
        conditions: Optional[Union[RuleCondition, List[RuleCondition]]] = None,
        destinations: Optional[Union[PathLike, List[PathLike]]] = None,
    ) -> None:
        self.conditions = conditions

        if not isinstance(self.conditions, List):
            self.conditions = [self.conditions]

        self.destinations = destinations

        if not isinstance(self.destinations, List):
            self.destinations = [self.destinations]

    def sort_folders(self: Self, folders: Union[PathLike, List[Path]]):
        if not isinstance(folders, List):
            folders = [folders]

        for folder in folders:
            ...

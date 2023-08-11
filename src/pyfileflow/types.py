import os
from pathlib import Path

from typing_extensions import Callable, TypeAlias, Union

from .fselements import FSElement

RuleCondition: TypeAlias = Callable[[FSElement], bool]
PathLike: TypeAlias = Union[Path, str, os.PathLike]

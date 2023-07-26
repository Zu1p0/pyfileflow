from pathlib import Path
from typing import List, Optional, Sequence, TypeAlias, Union

SUPPORTED_PATHS_TYPES: TypeAlias = Optional[
    Union[str, Path, Sequence[Union[str, Path]]]
]

PATH_LIST_TYPE: TypeAlias = List[Path]

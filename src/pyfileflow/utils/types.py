from pathlib import Path
from typing import List, Optional, Sequence, TypeAlias, Union

SupportedPathTypes: TypeAlias = Optional[
    Union[str, Path, Sequence[Union[str, Path]]]
]

PathListType: TypeAlias = List[Path]

from pathlib import Path
from typing import List, Optional, Sequence, TypeAlias, Union

try:
    from importlib.metadata import (PackageNotFoundError,  # type: ignore
                                    version)
except ImportError:  # pragma: no cover
    from importlib_metadata import (PackageNotFoundError,  # type: ignore
                                    version)

try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "Unknown"

from pyfileflow.fileorganizer import FileOrganizer



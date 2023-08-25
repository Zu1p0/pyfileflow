"""Utils.

Implement some utils functions.
"""

from typing import Any, List, Optional, Union


def parse_args(original_arg: Optional[Union[Any, List[Any]]]) -> List[Any]:
    """Parse input arguments into a list.

    This function takes one argument, which could be a single item or a list of items.
    It returns a list containing the parsed arguments, excluding any None values.

    Args:
        original_arg (Optional[Union[Any, List[Any]]]):
            The original argument(s) to be parsed.

    Returns:
        List[Any]:
            A list of parsed arguments without any None values.
    """
    parsed_arg = []
    if not isinstance(original_arg, list):
        parsed_arg = [original_arg]
    else:
        parsed_arg = original_arg

    parsed_arg = [arg for arg in parsed_arg if arg is not None]

    return parsed_arg

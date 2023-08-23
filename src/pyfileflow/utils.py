from typing import Any, Optional, Union


def parse_args(original_arg: Optional[Union[Any, list[Any]]]) -> list[Any]:
    parsed_arg = []
    if not isinstance(original_arg, list):
        parsed_arg = [original_arg]
    else:
        parsed_arg = original_arg

    parsed_arg = [arg for arg in parsed_arg if arg is not None]
    return parsed_arg

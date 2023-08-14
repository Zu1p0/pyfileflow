from typing_extensions import Callable

try:
    from typeguard import suppress_type_checks

except ImportError:

    def suppress_type_checks(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Callable:
            return func(*args, **kwargs)

        return wrapper

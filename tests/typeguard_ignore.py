"""Module providing compatibility for replacing typeguard's suppress_type_checks.

This module offers a dummy decorator 'suppress_type_checks' that serves as a 
replacement for the 'typeguard' module's 'suppress_type_checks' decorator. 
When 'typeguard' is not available, this dummy decorator allows tests to continue 
functioning without actual type checking.
"""

from typing_extensions import Callable

try:
    from typeguard import suppress_type_checks
except ImportError:

    def suppress_type_checks(func: Callable) -> Callable:
        """Dummy decorator for suppressing type checks.

        This decorator does not perform any type checking. It is provided as a dummy
        replacement when the 'typeguard' module is not available.

        Args:
            func (Callable): The function to be decorated.

        Returns:
            Callable: The input function, unchanged.
        """

        def wrapper(*args, **kwargs) -> Callable:
            return func(*args, **kwargs)

        return wrapper

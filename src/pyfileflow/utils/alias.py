from typing import Callable
import functools
from typing import Optional, Dict


def alias_class(klass: object):
    """
    Decorator to be used in combination with `@alias` decorator.
    Classes decorated with @aliased will have their aliased methods
    (via @alias) actually aliased.
    """
    methods = klass.__dict__.copy()
    for name, method in methods.items():
        if hasattr(method, "_aliases"):
            # add aliases but don't override attributes of 'klass'
            try:
                for alias in method._aliases - set(methods):
                    setattr(klass, alias, method)
            except TypeError:
                pass
    return klass


class alias_method(object):
    """
    Decorator for aliasing method names.
    Only works within classes decorated with '@alias_class'
    """

    def __init__(self, *aliases: str):
        self.aliases = set(aliases)

    def __call__(self, f: Callable):
        f._aliases = self.aliases
        return f


def alias_param(aliases : Optional[Dict[str, str]] = None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if aliases is not None:
                for name, alias in aliases.items():
                    if name not in kwargs and alias in kwargs:
                        kwargs[name] = kwargs[alias]
            return func(*args, **kwargs)

        return wrapper

    return decorator

from typing import Union

def alias_class(klass : object):
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


class alias(object):
    """
    Decorator for aliasing method names.
    Only works within classes decorated with '@alias_class'
    """

    def __init__(self, *aliases : str):
        self.aliases = set(aliases)

    def __call__(self, f):
        f._aliases = self.aliases
        return f

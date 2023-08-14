import pathlib


class Path(pathlib.Path):
    _flavour = type(pathlib.Path())._flavour

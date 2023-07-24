import pathlib

def clear_directory(path: pathlib.Path):
    for item in path.iterdir():
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            item.rmdir()
    return 0

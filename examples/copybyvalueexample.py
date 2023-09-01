"""Example on how to use the CopyByValueRule.

This sort all images in the unsorted folder in different folders depending on 
the time the photo was taken.
"""
from PIL import Image
from typing_extensions import Optional

from pyfileflow import CopyByValueRule
from pyfileflow.ppath import PPath


def get_date_taken(path: PPath) -> Optional[str]:
    """Function that returns the date the photo was taken.

    Args:
        path (PPath): The image path.

    Returns:
        Optional[str]: The date the photo was taken. None if the photo doesn't
        have exif data.
    """
    exif = Image.open(path)._getexif()
    if not exif:
        return None

    return exif[36867]


def check_image_extension(path: PPath) -> bool:
    """Function that checks if the file has an image extension.

    Args:
        path (PPath): the file path.

    Returns:
        bool: whether the file has an image extension or not.
    """
    return path.suffix() in (".jpg", ".png", ".jpeg")


rule = CopyByValueRule(
    condition=check_image_extension,
    destination="/images",
    sort_by=get_date_taken,
)

rule.process("/trash_folder")

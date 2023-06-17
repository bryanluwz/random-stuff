"""
Converts image type from one form to another
"""
import os
from PIL import Image
from constants import PIL_SUPPORTED_FORMATS


def convert_image_type(image_file_path, new_ext):
    if not os.path.exists(image_file_path):
        print(f"{image_file_path} does not exist. :< \n")
        return False

    new_ext = new_ext.lower().replace(".", "")

    if new_ext not in PIL_SUPPORTED_FORMATS:
        print(f"Extension of type {new_ext} is not supported. :/ \n")
        return False

    image = Image.open(image_file_path)

    new_file_path = os.path.splitext(image_file_path)[0] + f".{new_ext}"

    print(f"Saving new image to {new_file_path} :) \n")

    try:
        image.save(new_file_path)
    except Exception as e:
        print(f"Cannot save new image to {new_file_path} :( \n")
        return False

    return True

"""
Converts image type from one form to another
"""
from PIL import Image
import os
from argparse import ArgumentParser

PIL_SUPPORTED_FORMATS = [
        "bmp",
        "jpg",
        "jpeg",
        "j2k",
        "png",
        "tif",
        "tiff",
        "dds",
        "dib",
        "eps",
        "ico",
        "im",
        "pcx",
        "ppm",
        "pgm",
        "pbm",
        "pnm",
        "sgi",
        "tga",
        "tiff",
        "tif",
        "webp",
    ]

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
    except:
        print(f"Cannot save new image to {new_file_path} :( \n")
        return False

    return True

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-i", "--input", help="Input path of image", required=True)
    parser.add_argument("-e", "--extension", help="Extension type to be converted to", required=True)

    args = parser.parse_args()

    convert_image_type(args.input, args.extension)

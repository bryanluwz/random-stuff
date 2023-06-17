import os
from convert_image_type import convert_image_type
from constants import PIL_SUPPORTED_FORMATS

if __name__ == '__main__':
    input_file = None
    ext = None

    while not input_file:
        input_file = input("Enter input file path: ")
        try:
            input_file = input_file.replace("\"", "")
        except Exception as e:
            print(f"Cannot parse input file path. :< \n")
            input_file = None
        if not os.path.exists(input_file):
            print(f"{input_file} does not exist. :< \n")
            input_file = None

    while not ext:
        ext = input("Enter extension type to be converted to: ")
        ext = ext.lower().replace(".", "")
        if ext not in PIL_SUPPORTED_FORMATS:
            print(f"Extension of type {ext} is not supported. :/ \n")
            ext = None

        convert_image_type(input_file, ext)

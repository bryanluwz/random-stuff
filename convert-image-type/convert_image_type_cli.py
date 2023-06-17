from argparse import ArgumentParser
from convert_image_type import convert_image_type

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-i",
                        "--input",
                        help="Input path of image",
                        required=True)
    parser.add_argument("-e",
                        "--extension",
                        help="Extension type to be converted to",
                        required=True)

    args = parser.parse_args()

    convert_image_type(args.input, args.extension)

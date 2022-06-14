from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2
import os
import time

class IMG2ASCIIConverter:
    def __init__(self) -> None:
        self.image = None
        self.image_path = ""
        self.image_ascii_chars = ""
        self.ascii_image = None

        self.w = 1
        self.h = 1
        self.ideal_w = 240
        self.ideal_h = 240

        self.canvas_width = 0
        self.canvas_height = 0
        self.font = None
        self.line_height = 0

        self.gscale = [
            r'$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~i!lI;:,"^`. ',
            "@%#*+=-:. ",
        ]

    # Init functions
    def set_image(self, image_path: str):
        if not os.path.exists(image_path):
            image_path = os.path.join(
                os.path.dirname(os.path.realpath(__file__)), image_path
            )
            if not os.path.exists(image_path):
                print("Image file does not exist...")
                return

        self.image_path = image_path
        self.image = cv2.imread(image_path, 0)
        self.h, self.w = self.image.shape

    def set_image_by_cv2im_array(self, image_array):
        self.image = image_array
        self.h, self.w = self.image.shape

    def set_ideal_scale(self, w, h):
        self.ideal_w, self.ideal_h = w, h

    def show_image(self):
        if self.image is None:
            return

        cv2.imshow("Image", self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # Conversion
    def convert_IMG2ASCII(self, fpath="", gscale=0):
        if fpath == "":
            output_path = os.path.splitext(self.image_path)[0] + ".txt"
        elif fpath is not None:
            output_path = os.path.splitext(fpath)[0] + ".txt"

        self.final_scale_image()
        image_ascii_chars = self.get_chars_from_grayscale_img(
            self.gscale[gscale], self.image
        )
        self.image_ascii_chars = image_ascii_chars

        if fpath is not None:
            self.write_to_txt(output_path, self.image_ascii_chars)

        return image_ascii_chars

    def get_chars_from_grayscale_img(self, gscale, img_arr, max_value=256, min_value=0):
        img_chars = ""
        gscale_len = len(gscale)

        for i in img_arr:
            for j in i:
                img_chars += gscale[
                    int((j / (max_value - min_value) + min_value) * gscale_len)
                ]
            img_chars += "\n"

        return img_chars

    def write_to_txt(self, path_name, data):
        with open(path_name, "w") as f:
            f.write(data)

    # Scale image
    def scale_image_ratio(self, scale_ratio):
        self.image = cv2.resize(
            self.image,
            (int(self.w * scale_ratio), int(self.h * scale_ratio)),
            interpolation=cv2.INTER_AREA,
        )
        self.h, self.w = self.image.shape

    def scale_image_pixels(self, w, h):
        self.image = cv2.resize(self.image, (w, h), interpolation=cv2.INTER_AREA)
        self.h, self.w = self.image.shape

    def auto_scale(self):
        scale_ratio = min((self.ideal_w / self.w), (self.ideal_h / self.h))
        self.scale_image_ratio(scale_ratio)

    def final_scale_image(self, w2h_ratio=5 / 2):
        """
        Scale image before conversion so that final image does not look scaled
        """
        self.image = cv2.resize(
            self.image, (int(self.w * w2h_ratio), self.h), interpolation=cv2.INTER_AREA
        )
        self.h, self.w = self.image.shape

    # Save generated ascii text to image
    def save_to_img(self, gscale=0, upscale=1, custom_ascii=None):
        if self.image_ascii_chars == "" and custom_ascii is not None:
            self.convert_IMG2ASCII(fpath=None, gscale=gscale)

        # Lines of ASCII
        if custom_ascii is not None:
            lines = custom_ascii
        else:
            lines = self.image_ascii_chars.split("\n")

        # Prepare font
        fontsize = int(1000 / self.ideal_w) * upscale

        if self.font is None:
            self.font = ImageFont.truetype("./consola.ttf", size=fontsize)

        # Get max width and heights of line to create canvas
        if self.canvas_width == 0 and self.canvas_height == 0:
            font_points_to_pixels = lambda pt: round(pt * 96 / 72)

            widest_line = max(lines, key=lambda s: self.font.getsize(s)[0])
            widest_line_width = font_points_to_pixels(self.font.getsize(widest_line)[0])

            tallest_line = max(lines, key=lambda s: self.font.getsize(s)[1])
            tallest_line_height = font_points_to_pixels(self.font.getsize(tallest_line)[1])
            line_height = tallest_line_height * 1.05
            self.line_height = line_height

            self.canvas_width = int(widest_line_width * 0.75)
            self.canvas_height = int(line_height * len(lines))

        # Writing text on image
        canvas = Image.new("RGB", (self.canvas_width, self.canvas_height), (255, 255, 255))
        d = ImageDraw.Draw(canvas)

        for i in range(len(lines)):
            d.text((0, i * self.line_height * 1.01), lines[i], fill=(0, 0, 0), font=self.font)

        self.ascii_image = canvas
        return self.ascii_image

    def write_to_img(self, pil_img=None, fpath="", ext="jpg"):
        # Create output path for image
        if fpath == "":
            output_path = os.path.splitext(self.image_path)[0] + "." + ext
        else:
            output_path = os.path.splitext(fpath)[0] + "." + ext

        # Save image
        if pil_img is None:
            if self.ascii_image is None:
                pil_img = self.save_to_img()
            else:
                pil_img = self.ascii_image

        pil_img.save(output_path)


if __name__ == "__main__":
    t0 = time.time()
    converter = IMG2ASCIIConverter()
    converter.set_ideal_scale(100, 100)
    converter.set_image(".\\test_folder\\rick_astley.png")
    converter.auto_scale()
    converter.convert_IMG2ASCII(gscale=0, fpath=None)
    converter.save_to_img(gscale=1)
    converter.write_to_img()
    print(f"{time.time() - t0}s")

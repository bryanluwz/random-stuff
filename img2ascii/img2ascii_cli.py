from argparse import ArgumentParser
import img2ascii
import vid2ascii

if __name__ == '__main__':
    parser = ArgumentParser(description="Image / Video to ASCII ART")

    parser.add_argument("-v", "--video-file", help="Target video file")
    parser.add_argument("-i", "--image-file", help="Target image file")
    parser.add_argument("-iw", "--ideal-width", help="Ideal chars for ASCII output width", default=100)
    parser.add_argument("-ih", "--ideal-height", help="Ideal chars for ASCII output height", default=100)
    parser.add_argument("-g", "--gscale-level", help="Type of ASCII scale to be used", default=0)
    parser.add_argument("-vid", "--is-video", help="Is type video or not", default=False, action="store_true")
    parser.add_argument("-o", "--output", help="output_path")
    parser.add_argument("-ot", "--temp-output", help="temp_output_path")
    parser.add_argument("-d", "--debug", default=False, action="store_true")

    args = parser.parse_args()

    converter = None

    if args.is_video:
        converter = vid2ascii.VID2ASCIIConverter()
        converter.set_ideal_scale(args.ideal_width, args.ideal_height)
        converter.set_video_path(args.video_file)
        if args.output:
            converter.video_output_path = args.output
        if args.temp_output:
            converter.video_output_path = args.temp_output
        converter.vid_to_ascii_frames(gscale=args.gscale_level, write_frames_and_append=False)
        converter.add_original_soundtrack(del_temp=not args.debug)

    else:
        converter = img2ascii.IMG2ASCIIConverter()
        converter.set_ideal_scale(args.ideal_width, args.ideal_height)
        converter.set_image(args.image_file)
        converter.auto_scale()
        converter.save_to_img(gscale=args.gscale_level)
        converter.write_to_img()
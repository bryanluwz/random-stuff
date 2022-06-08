import cv2
import os
import imageio
import numpy as np
import shutil
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip

import img2ascii


class VID2ASCIIConverter:
    def __init__(self) -> None:
        self.img2ascii_converter = img2ascii.IMG2ASCIIConverter()
        self.img2ascii_converter.set_ideal_scale(50, 50)

        self.writer = None

        self.video_path = ""
        self.video_output_path = ""
        self.temp_video_output_path = "./out.mp4"
        self.frames_output_dir = ""
        self.fps = 1
        self.frame_count = 0       

    def set_ideal_scale(self, ideal_w, ideal_h):
        self.img2ascii_converter.set_ideal_scale(ideal_w, ideal_h)

    def set_video_path(self, video_path):
        # Set the output path for frames
        self.video_path = video_path
        # self.frames_output_dir = os.path.join(os.path.dirname(self.video_path), f'{os.path.splitext(self.video_path)[0] + "_frames"}')
        self.frames_output_dir = "./frames/"

        self.video_output_path = os.path.splitext(self.video_path)[0] + "_ascii.mp4"

    def vid_to_ascii_frames(self, gscale=0, ext='jpg', write_frames_and_append=False):
        # Start reading video until ret == 0
        video_capture = cv2.VideoCapture(self.video_path)
        self.fps = video_capture.get(cv2.CAP_PROP_FPS)
        self.frame_count = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)

        # How many digits does the frame name needs
        frame_name_num_length = len(str(int(self.frame_count)))

        ret, frame = video_capture.read()

        # Mkdir, if dir exists, prompt user
        if write_frames_and_append:
            if not os.path.isdir(self.frames_output_dir):
                os.mkdir(self.frames_output_dir)
            elif os.path.isdir(self.frames_output_dir):
                if input("Directory already exist, overwrite (N?) ").lower() == 'n':
                    return

        i = 0

        while ret:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            self.img2ascii_converter.set_image_by_cv2im_array(gray_frame)
            
            # Add frames into frames arrat
            self.img2ascii_converter.auto_scale()
            
            frame_name = f'frame_{i:0{frame_name_num_length}d}.{ext}'
            output_path = os.path.join(self.frames_output_dir, frame_name)

            self.img2ascii_converter.convert_IMG2ASCII(fpath=None)
            ascii_frame = self.img2ascii_converter.save_to_img(gscale=gscale)
            
            if write_frames_and_append:
                self.write_frames_to_folder(frame=ascii_frame, fpath=output_path)
            else:
                if self.writer is None or self.writer.closed:
                    self.writer = imageio.get_writer(self.temp_video_output_path, fps=self.fps)
                
                self.append_frame_to_out(frame=np.array(ascii_frame), writer=self.writer)            

            ret, frame = video_capture.read()
            
            i += 1
            print(f"Frame {i} out of {int(self.frame_count)} completed")

        self.writer.close()


    def write_frames_to_folder(self, frame, fpath):
        frame.save(fpath)

    def frames_to_mp4(self, frames_dir="", fps=None, ext='jpg'):
        if frames_dir == "":
            frames_dir = self.frames_output_dir

        if fps is None:
            fps = self.fps

        writer = imageio.get_writer(self.temp_video_output_path, fps=fps)
        for file in os.listdir(frames_dir):
            im = imageio.imread(os.path.join(frames_dir, file))
            writer.append_data(im)
        
        writer.close()

    def append_frame_to_out(self, frame, writer):
        im = frame
        writer.append_data(im)

    def delete_frames(self):
        if os.path.isdir(self.frames_output_dir):
            shutil.rmtree(self.frames_output_dir)

    def add_original_soundtrack(self, del_temp=True):
        video_clip = VideoFileClip(self.temp_video_output_path)
        audio_clip = AudioFileClip(self.video_path)    
        video_clip = video_clip.set_audio(audio_clip)
        video_clip.write_videofile(self.video_output_path)

        if del_temp:
            os.remove(self.temp_video_output_path)
    
if __name__ == '__main__':
    vid2ascii_converter = VID2ASCIIConverter()
    vid2ascii_converter.set_ideal_scale(50, 50)
    vid2ascii_converter.set_video_path("./test_folder/chika_dance_Trim.mp4")
    # vid2ascii_converter.vid_to_ascii_frames(write_frames_and_append=False)

    # Call this if write frames and append is set to true, that will write individual frames down to a file
    vid2ascii_converter.frames_to_mp4()
    vid2ascii_converter.delete_frames()

    vid2ascii_converter.add_original_soundtrack(del_temp=False)
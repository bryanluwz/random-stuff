use image::RgbImage;
use opencv::{imgcodecs, prelude::*};
use rusttype::Font;
use std::env;
use std::time::Instant;

pub mod img2ascii_converter_module {
    use image::{self, Rgb, RgbImage};
    use opencv::{core, highgui, imgcodecs, imgproc, prelude::*, Result};
    use rusttype::{Font, Scale};
    use std::fs::File;
    use std::io::{Error, Write};
    use std::path::Path;
    use std::time::Instant;

    // Struct for IMG2ASCII Converter
    pub struct IMG2ASCIIConverter {
        pub image: Mat,
        pub image_path: String,
        pub image_ascii_chars: String,
        pub ascii_image: String,

        pub w: i32,
        pub h: i32,
        pub ideal_w: i32,
        pub ideal_h: i32,

        pub canvas_template: RgbImage,
        pub is_canvas_template_ready: bool,
        pub canvas_width: i32,
        pub canvas_height: i32,
        pub line_height: f32,
        pub font: Font<'static>,

        pub gscale: Vec<String>,
        pub gscale_level: i32,
    }

    // Implementation for IMG2ASCII Converter
    impl IMG2ASCIIConverter {
        // Tester function
        pub fn print_info(&self) {
            println!("Image path: {}", self.image_path);
            println!("Image ASCII chars length: {}", self.image_ascii_chars.len());
            println!("Image path: {}", self.w);
            println!("Image path: {}", self.h);
            println!("Image path: {}", self.ideal_w);
            println!("Image path: {}", self.ideal_h);
        }

        // Set converter to default settings
        pub fn init(&mut self) {
            self.image = Mat::default();
            self.image_path = String::new();
            self.image_ascii_chars = String::new();
            self.ascii_image = String::new();

            self.w = -1;
            self.h = -1;
            self.ideal_w = 100;
            self.ideal_h = 100;

            self.canvas_width = -1;
            self.canvas_height = -1;
            self.line_height = 10.0;
            self.font =
                Font::try_from_vec(Vec::from(include_bytes!("./consola.ttf") as &[u8])).unwrap();

            self.gscale = vec![
                String::from(
                    "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~i!lI;:,\"^`. ",
                ),
                String::from("@%#*+=-:. "),
            ];

            self.gscale_level = 0;
        }

        // Set the image by image_path
        pub fn set_image(&mut self, image_path: &str) -> Result<(), opencv::Error> {
            self.image = imgcodecs::imread(image_path, 0).unwrap();
            self.image_path = image_path.to_string();
            self.update_image_width_height();
            return Ok(());
        }

        // Set the image by image matrix
        pub fn set_image_by_matrix(&mut self, image_array: Mat) -> Result<(), opencv::Error> {
            self.image = image_array;
            self.update_image_width_height();
            return Ok(());
        }

        // Update image width and height variables
        pub fn update_image_width_height(&mut self) {
            (self.w, self.h) = (
                self.image.size().unwrap().width,
                self.image.size().unwrap().height,
            );
        }

        // Set the ideal scale of the converter
        pub fn set_ideal_scale(&mut self, w: i32, h: i32) {
            self.ideal_w = w;
            self.ideal_h = h;
        }

        // Set the gscale level of the converter
        pub fn set_gscale_level(&mut self, gscale_level: i32) {
            self.gscale_level = gscale_level;
        }

        // Shows image to screen
        pub fn show_image(&mut self) -> Result<(), opencv::Error> {
            highgui::imshow("window", &self.image)?;
            highgui::wait_key(0)?;
            return Ok(());
        }

        // Scaling functions
        pub fn scale_image_by_ratio(
            &mut self,
            scale_ratio_x: f64,
            scale_ratio_y: f64,
        ) -> Result<(), opencv::Error> {
            let mut scaled_image = Mat::default();
            imgproc::resize(
                &self.image,
                &mut scaled_image,
                core::Size {
                    width: 0,
                    height: 0,
                },
                scale_ratio_x,
                scale_ratio_y,
                imgproc::INTER_LINEAR,
            )?;
            self.image = scaled_image;
            self.update_image_width_height();
            return Ok(());
        }

        pub fn auto_scale(&mut self) -> Result<(), opencv::Error> {
            let scale_ratio: f64 = f64::min(
                (self.ideal_w as f64) / (self.w as f64),
                (self.ideal_h as f64) / (self.h as f64),
            );
            self.scale_image_by_ratio(scale_ratio, scale_ratio)?;
            return Ok(());
        }

        pub fn final_scale(&mut self) -> Result<(), opencv::Error> {
            let w2h_ratio: f64 = 2.5;
            self.scale_image_by_ratio(w2h_ratio, 1.0)?;
            return Ok(());
        }

        // Converting image to ASCII main function
        pub fn convert_image_to_ascii(&mut self, output_path: &str) -> Result<(), Error> {
            self.get_chars_from_gray_image(self.gscale_level);

            if str::ends_with(output_path, ".txt") {
                self.write_to_text_file(output_path)?;
            }

            return Ok(());
        }

        // Converting image to ASCII helper function
        pub fn get_chars_from_gray_image(&mut self, gscale_level: i32) -> String {
            let max_gray_value: i32 = 256;
            let min_gray_value: i32 = 0;

            let mut image_ascii_chars: String = String::new();

            let gscale_string = &(self.gscale[gscale_level as usize]);
            let gscale_string_length = gscale_string.len();

            for i in 0..self.image.size().unwrap().height {
                for j in 0..self.image.size().unwrap().width {
                    let appended_char =
                        gscale_string.as_bytes()[(((*(self.image).at_2d_mut::<u8>(i, j).unwrap()
                            as f32)
                            / ((max_gray_value as f32) - (min_gray_value as f32)))
                            * (gscale_string_length as f32))
                            as usize] as char;
                    image_ascii_chars.push(appended_char);
                }
                image_ascii_chars.push('\n');
            }

            self.image_ascii_chars = format!("{}", image_ascii_chars);

            return self.image_ascii_chars.clone();
        }

        pub fn write_to_text_file(&self, output_path: &str) -> Result<(), Error> {
            let mut output = File::create(output_path)?;
            writeln!(output, "{}", format!("{}", self.image_ascii_chars))?;
            return Ok(());
        }

        pub fn save_to_image_file_imageproc(&mut self, output_path: &str) {
            // Set scale of font
            let scale = Scale {
                x: self.line_height,
                y: self.line_height,
            };

            // Grab text width and total height to create our canvas template
            // When we draw text we can just clone the canvas
            let text_list = self.image_ascii_chars.split("\n").collect::<Vec<&str>>();
            let mut text = text_list[0];

            if (self.canvas_width == -1) || (self.canvas_height == -1) {
                // Only calculate the canvas width and height if it has not been calculated before
                let (w, _h) = imageproc::drawing::text_size(scale, &self.font, text);
                self.canvas_width = w;
                self.canvas_height =
                    (self.line_height as f32 * text_list.len() as f32 * 1.35) as i32;

                // Create empty canvas and set it to white
                let mut canvas =
                    image::RgbImage::new(self.canvas_width as u32, self.canvas_height as u32);

                imageproc::drawing::draw_filled_rect_mut(
                    &mut canvas,
                    imageproc::rect::Rect::at(0, 0)
                        .of_size(self.canvas_width as u32, self.canvas_height as u32),
                    Rgb([255u8, 255u8, 255u8]),
                );

                self.canvas_template = canvas;
            }

            // Clone a new canvas
            let mut canvas = self.canvas_template.clone();

            // remove this
            let mut start = Instant::now();

            // Draw text
            for line_count in 0..text_list.len() {
                text = text_list[line_count];
                    imageproc::drawing::draw_text_mut(
                    &mut canvas,
                    Rgb([0u8, 0u8, 0u8]),
                    0,
                    (self.line_height * line_count as f32 * 1.37) as i32,
                    scale,
                    &self.font,
                    text,
                );
            }

            let elapsed = start.elapsed();
            println!("Drawing text took {:?}", elapsed);
            start = Instant::now();

            // Save to output path (make sure ends with .jpg)
            if !(output_path.ends_with(".jpg")) {
                output_path.to_string().push_str(".jpg");
            }

            let _ = canvas.save(Path::new(&*output_path)).unwrap();

            let elapsed = start.elapsed();
            println!("Saving image took {:?}", elapsed);
        }

    }
}

pub mod vid2ascii_converter_module {
    use image::{self, Rgb, RgbImage};
    use opencv::{core, highgui, imgcodecs, imgproc, prelude::*, Result, videoio};
    use rusttype::{Font, Scale};
    use std::fs::File;
    use std::io::{Error, Write};
    use std::path::Path;
    use std::time::Instant;


    use crate::img2ascii_converter_module;

    pub struct VID2ASCIIConverter {
        pub img2ascii_converter: img2ascii_converter_module::IMG2ASCIIConverter,
        pub video_path: String,
        pub fps: f64,
        pub total_frame_count: i32,
    }

    impl VID2ASCIIConverter {
        // Initialise converter
        pub fn init_converter(&mut self) {
            self.img2ascii_converter.init();
            self.img2ascii_converter.set_ideal_scale(100, 100);
        }

        // Set the video using opencv   
        pub fn set_video(&mut self, video_path:&str) {
            let mut video = videoio::VideoCapture::from_file(video_path, videoio::CAP_ANY).expect("Failed to load video");
            self.total_frame_count = video.get(videoio::CAP_PROP_FRAME_COUNT).unwrap() as i32;
            self.fps = video.get(videoio::CAP_PROP_FPS).unwrap() as f64;
            let mut frame = core::Mat::default();
            let mut ret:bool = false;
            let mut frame_count = 0;

            for i in 0..10 {
                video.read(&mut frame);
                let mut gray = core::Mat::default();
                opencv::imgproc::cvt_color(&frame, &mut gray, opencv::imgproc::COLOR_BGR2GRAY, 0);
                self.img2ascii_converter.set_image_by_matrix(gray.clone());
                self.img2ascii_converter.auto_scale();
                self.img2ascii_converter.final_scale();
                self.img2ascii_converter.convert_image_to_ascii("");
                self.img2ascii_converter.save_to_image_file_imageproc(&*format!("{:0>5}.jpg", frame_count));
                frame_count += 1;
            }

        }
    }
}

use img2ascii_converter_module::IMG2ASCIIConverter;
use vid2ascii_converter_module::VID2ASCIIConverter;
fn main() {
    // Time the program
    let mut start = Instant::now();

    // Get file path
    let args: Vec<String> = env::args().collect();
    let input_path = &args[1];
    let output_path = &args[2];

    let mut img2ascii_converter: IMG2ASCIIConverter = IMG2ASCIIConverter {
        image: Mat::default(),
        image_path: String::from("Some string"),
        image_ascii_chars: String::from("Some string"),
        ascii_image: String::from("Some string"),

        w: 1,
        h: 1,
        ideal_w: 1,
        ideal_h: 1,

        canvas_template: RgbImage::new(1, 1),
        is_canvas_template_ready: false,
        canvas_width: -1,
        canvas_height: -1,
        line_height: -1.0,
        font: Font::try_from_vec(Vec::from(include_bytes!("./consola.ttf") as &[u8])).unwrap(),

        gscale: vec![],
        gscale_level: 0,
    };

    // img2ascii_converter.init();

    // img2ascii_converter.set_ideal_scale(100, 100);

    // let image_frame = imgcodecs::imread(input_path, 0).unwrap();
    // img2ascii_converter
    //     .set_image_by_matrix(image_frame)
    //     .expect("Error when setting image via matrix");

    // img2ascii_converter
    //     .auto_scale()
    //     .expect("Error when auto scaling image");

    // img2ascii_converter.final_scale().expect("Error when scaling image");

    // let elapsed = start.elapsed();
    // println!("Setting up took {:?}", elapsed);
    // start = Instant::now();

    // // converter.show_image().expect("Error when showing image");

    // img2ascii_converter
    //     .convert_image_to_ascii("out")
    //     .expect("Error when converting image to ASCII chars");

    // let elapsed = start.elapsed();
    // println!("Conversion took {:?}", elapsed);
    // start = Instant::now();

    // img2ascii_converter.save_to_image_file_imageproc(output_path);

    // let elapsed = start.elapsed();
    // println!("Overall drawing and saving took {:?}", elapsed);

    let mut vid2ascii_converter: VID2ASCIIConverter = VID2ASCIIConverter {
        img2ascii_converter: img2ascii_converter,
        video_path: String::new(),
        fps: -1.0,
        total_frame_count: -1,
    };
    
    vid2ascii_converter.init_converter();
    vid2ascii_converter.set_video(input_path);
}

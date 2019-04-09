from symbolic_aggregate_approximation import SymbolicAggregateApproximation
from bitmap_module.rgb_letter_to_colour_conversion import rgb_letter_to_colour
from bitmap_module.greyscale_letter_to_colour_conversion import greyscale_letter_to_colour
from bitmap_module.text_to_bmp_class import Bitmap
from PIL import Image
import os

import sys
sys.path.append("../")
from logger_module.Logger import Logger

class BitmapGenerator:

    # TODO: Low this to 32 x 32  or 48 x 48 -- 2 Seconds and 4 seconds respectively; 100x100 corresponds to 40 seconds... bad...
    bitmap_size = 100

    image_map = {
        'train' : {
            'Walk' : 0,
            'Run' : 0,
            'LowResistanceBike' : 0,
            'HighResistanceBike' : 0
        },
        'test' : {
            'Walk' : 0,
            'Run' : 0,
            'LowResistanceBike' : 0,
            'HighResistanceBike' : 0
        }
    }

    server_image_counter = 0

    def __init__(self, colour="greyscale", logger_path="../../"):
        self.sax_obj = SymbolicAggregateApproximation(False)
        self.colour = colour
        
        # Logger
        self.logger = Logger(logger_path, "logs/BitmapGenerator")

    def build(self):
        # Train
        self.generate_bitmaps('train', 1, 2)
        self.generate_bitmaps('train', 3, 4)
        self.generate_bitmaps('train', 4, 7)

        # Test Subject #2 - Because we can guarantee all activities are from the same subject.
        self.generate_bitmaps('test', 2, 3)

    def generate_bitmaps(self, data_type, start, end):
        for index in range(start, end):
            try:
                walk_sax_str = self.sax_obj.generate_walk(index)
                self.generate_all("Walk", walk_sax_str, index, data_type)

                run_sax_str = self.sax_obj.generate_run(index)
                self.generate_all("Run", run_sax_str, index, data_type)

                low_bike_sax_str = self.sax_obj.generate_low_bike(index)
                self.generate_all("LowResistanceBike", low_bike_sax_str, index, data_type)

                high_bike_sax_str = self.sax_obj.generate_high_bike(index)
                self.generate_all("HighResistanceBike", high_bike_sax_str, index, data_type)

            except FileNotFoundError:
                self.logger.warning("File not found with ID: (" + str(index) + ")")

    def generate_all(self, activity, sax_string, count, data_type):
        # Move up the sax_string by some 'shift' amount, each image will have some portion of the previous image within it.
        shift = 16
        for i in range(0, len(sax_string), shift):
            pos_in_string = i // shift

            # 80% / 20% for train and test respectively.
            self.generate(activity, sax_string, pos_in_string, shift, data_type)

        if data_type == 'train':
            self.logger.info("Training {} (Subject #{}) complete - bitmaps for activity total: {}".format(activity, count, self.image_map["train"][activity]))
        else:
            self.logger.info("Testing {} (Subject #{}) complete - bitmaps for activity total: {}".format(activity, count, self.image_map["test"][activity]))

    def generate(self, activity, sax_string, pos_in_string, shift, data_group):

        # Image size: 100x100
        image = Bitmap(self.bitmap_size, self.bitmap_size)

        # Try and Except - Except needed when iterations extend passed the SAX string length. 
        try:
            for row in range(self.bitmap_size):
                for col in range(self.bitmap_size):
                    # We set each pixel in the bitmap based on the mapping function, from the bitmap_module.
                    letter_choice = (shift * pos_in_string) + (row * self.bitmap_size) + col
                    if (self.colour == "rgb"):
                        image_colour = rgb_letter_to_colour(sax_string[letter_choice])
                    else:
                        image_colour = greyscale_letter_to_colour(sax_string[letter_choice])

                    image.setPixel(row, col, image_colour)

            # Tend towards data-group: increment image counters
            self.image_map[data_group][activity] += 1
            count = self.image_map[data_group][activity]

            # Finally, write the bitmaps to the correct location (train/test)
            save_location = './pixel_bitmaps/' + data_group + '/' + activity + '/' + activity + '-{}-{}'.format(data_group, count)
            image.write(save_location + ".bmp")

            # Convert to JPEG - Must be JPEG for inception model.
            img = Image.open(save_location + ".bmp")
            new_img = img.resize( (128, 128), Image.ANTIALIAS )

            new_img.save(save_location + ".jpeg", 'jpeg')
            os.remove(save_location + ".bmp")
        except Exception as e:
            pass

    # Function designed for incoming sax strings from clients
    # simply only takes a symbol string of SAX characters and converts to an image
    # Saves temporarily on server in ./temp
    # Colour is greyscale by default; Can be changed via the function call.
    # TODO: Test this
    def generate_single_bitmap(self, symbolic_string):
        
        # Image size: 100x100
        image = Bitmap(self.bitmap_size, self.bitmap_size)

        # Try and Except - Except needed when iterations extend passed the SAX string length. 
        try:
            for row in range(self.bitmap_size):
                for col in range(self.bitmap_size):
                    # We set each pixel in the bitmap based on the mapping function, from the bitmap_module.
                    letter_choice = (row * self.bitmap_size) + col
                    if (self.colour == "rgb"):
                        pixel_colour = rgb_letter_to_colour(symbolic_string[letter_choice])
                    else:
                        pixel_colour = greyscale_letter_to_colour(symbolic_string[letter_choice])

                    image.setPixel(row, col, pixel_colour)

            save_location = "./temp/activity-{}".format(self.server_image_counter)
            image.write(save_location + ".bmp")
            self.server_image_counter += 1

            # Convert to JPEG - Must be JPEG for inception model.
            img = Image.open(save_location + ".bmp")
            new_img = img.resize( (128, 128), Image.ANTIALIAS )

            new_img.save(save_location + ".jpeg", 'jpeg')
            os.remove(save_location + ".bmp")
        except Exception as e:
            pass

    def reset_activity_counter(self):
        self.server_image_counter = 0

if __name__ == "__main__":
    x = BitmapGenerator()
    x.build()
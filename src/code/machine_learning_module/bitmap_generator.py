# os module used for removing .bmp files - Google Inception only works with PNG/JPEG
import os
# Import sys for pathing related problems
import sys
sys.path.append("./code/machine_learning_module")
# Imports from other project related modules
from symbolic_aggregate_approximation import SymbolicAggregateApproximation
from bitmap_module.rgb_letter_to_colour_conversion import rgb_letter_to_colour
from bitmap_module.greyscale_letter_to_colour_conversion import greyscale_letter_to_colour
from bitmap_module.text_to_bmp_class import Bitmap
# Pil for image compression and resizing
from PIL import Image
# Set the path to the module coordinator directory 1 above.
sys.path.append("../")
# Logger for logging adequately and saving results
from logger_module.Logger import Logger

class BitmapGenerator:

    # Size of each individual training and testing bitmap
    # TODO: Low this to 32 x 32  or 48 x 48 -- 2 Seconds and 4 seconds respectively; 100x100 corresponds to 40 seconds... bad...
    bitmap_size = 32

    # A mapping to track how many images have been generated for each mode (train/test) and each class of that mode.
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

    # Variable used by the server-side component of the project.
    server_image_counter = 0

    def __init__(self, colour="greyscale", logger_path="../", testMode=False):
        # Symbolic Aggregate Approximation object for conversion to string then to bitmap.
        self.sax_obj = SymbolicAggregateApproximation(False)
        # Training subjects - [3] results in good Walk/HighBike Generalization. 
        self.train_subjects = [1, 2, 3, 4, 5, 7, 8, 9]
        # Test Subject #2 - Because we can guarantee all activities are from the same subject.
        self.test_subjects = [6]
        # Colour of bitmaps when generated
        self.colour = colour
        # Logger
        self.logger = Logger(logger_path, "logs/BitmapGenerator", testMode)

    # Build the training and Testing JPEGs - Generally takes some time.
    def build(self):
        # Train on all passed in subjects
        for subject in self.train_subjects:
            self.generate_bitmaps('train', subject)
        # Test on all passed in subjects (Generally only 1 subject to test - leave 1 subject out cross validation)
        for subject in self.test_subjects:
            self.generate_bitmaps('test', subject)

    # Method to generate individual subjct activity results as a bitmap form.
    def generate_bitmaps(self, mode, subject):
        try:
            self.generate_bitmaps_for_subject(mode, subject)
        except FileNotFoundError:
            self.logger.warning("Subject #{} not found for mode: {}".format(subject, mode))

    # Method which applies the necessary logic to generate the bitmap image for a subject for all activities performed.
    def generate_bitmaps_for_subject(self, mode, subject):
        sax_activity_representations = self.sax_obj.generate_all_activities_as_string_representation(subject)
        for index, activity_key in enumerate(self.image_map[mode]):
            activity_repr = sax_activity_representations[index]
            self.generate_all(activity_key, activity_repr, subject, mode)

    # Method passes the correct substrings into the generate method and also logs when all bitmaps related to a particular subject
    # For a given activity have been completed. 
    def generate_all(self, activity, sax_string, count, mode):
        # Each image will have some portion of the previous image within it.
        # This counter can dictate how similar or dissimilar each successive image generated is.
        # The higher this value, the more images, but the more similar they will be.
        shift = 64
        
        for position in range(0, len(sax_string), shift):
            pos_in_string = position // shift

            # 80% / 20% for train and test respectively.
            self.generate(activity, sax_string, pos_in_string, shift, mode)

        if mode == 'train':
            self.logger.info("Training {} (Subject #{}) complete - bitmaps for activity total: {}".format(activity, count, self.image_map["train"][activity]))
        else:
            self.logger.info("Testing {} (Subject #{}) complete - bitmaps for activity total: {}".format(activity, count, self.image_map["test"][activity]))

    # Method which builds and places bitmaps for a given candidate in the necessary mode class folders.
    # Method has many variables to improve accuracy of the model.
    # Images can be generated larger or smaller
    # Images can be generated as greyscale or RGB with different parameters.
    # Images are, once fully generated, saved correctly to the necessary train/test folders.
    def generate(self, activity, sax_string, pos_in_string, shift, mode):

        # Try and Except - Except needed when iterations extend passed the SAX string length. 
        try:
            # Build image via setting each pixel
            image = self.build_image(shift, pos_in_string, sax_string)

            # Tend towards data-group: increment image counters
            self.image_map[mode][activity] += 1
            count = self.image_map[mode][activity]

            # Finally, write the bitmaps to the correct location (train/test)
            save_location = './pixel_bitmaps/' + mode + '/' + activity + '/' + activity + '-{}-{}'.format(mode, count)
            image.write(save_location + ".bmp")

            # Convert to JPEG - Must be JPEG for inception model.
            img = Image.open(save_location + ".bmp")
            new_img = img.resize( (128, 128), Image.ANTIALIAS )

            new_img.save(save_location + ".jpeg", 'jpeg')
            os.remove(save_location + ".bmp")
        except Exception as e:
            pass

    def build_image(self, shift, pos_in_string, sax_string):
        # Image size: 100x100
        # Uses global variable to dictate size of bitmap.
        bitmap = Bitmap(self.bitmap_size, self.bitmap_size)

        for row in range(self.bitmap_size):
            for col in range(self.bitmap_size):
                # We set each pixel in the bitmap based on the mapping function, from the bitmap_module.
                letter_choice = (shift * pos_in_string) + (row * self.bitmap_size) + col
                if (self.colour == "rgb"):
                    image_colour = rgb_letter_to_colour(sax_string[letter_choice])
                else:
                    image_colour = greyscale_letter_to_colour(sax_string[letter_choice])

                # Individually set each pixel with the appropriate colour, based on the sax string character.
                bitmap.setPixel(row, col, image_colour)
        return bitmap

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

    def generate_single_bitmap_real_time(self, symbolic_string):
        
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

            save_location = "./temp/activity-{}".format(0)
            image.write(save_location + ".bmp")

            # Convert to JPEG - Must be JPEG for inception model.
            img = Image.open(save_location + ".bmp")
            new_img = img.resize( (128, 128), Image.ANTIALIAS )

            new_img.save(save_location + ".jpeg", 'jpeg')
            os.remove(save_location + ".bmp")
        except Exception as e:
            pass

    # Simple reset method for the server image counter.
    def reset_activity_counter(self):
        self.server_image_counter = 0

    # Destroy temp folder
    def destroy_temp_folder(self):
        files = glob.glob('../mqtt_protocol_module/temp/*')
        for f in files:
            os.remove(f)

if __name__ == "__main__":
    generator = BitmapGenerator()
    generator.build()
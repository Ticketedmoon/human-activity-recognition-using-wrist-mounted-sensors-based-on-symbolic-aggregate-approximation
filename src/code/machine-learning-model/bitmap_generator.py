from symbolic_aggregate_approximation import SymbolicAggregateApproximation
from bitmap_module.letter_to_colour_conversion import letter_to_colour
from bitmap_module.text_to_bmp_class import Bitmap

class BitmapGenerator:

    bitmap_size = 32

    def __init__(self):
        self.sax_obj = SymbolicAggregateApproximation()

    def generate_bitmaps(self):
        for index in range(1, 7):
            try:
                print("Activity level: " + str(index))
                walk_sax_str = self.sax_obj.generate_walk(index)
                self.generate_all("Walk", walk_sax_str, index)

                run_sax_str = self.sax_obj.generate_run(index)
                self.generate_all("Run", run_sax_str, index)

                low_bike_sax_str = self.sax_obj.generate_low_bike(index)
                self.generate_all("LowResistanceBike", low_bike_sax_str, index)

                high_bike_sax_str = self.sax_obj.generate_high_bike(index)
                self.generate_all("HighResistanceBike", high_bike_sax_str, index)

            except FileNotFoundError:
                print("File not found with ID: (" + str(index) + ")")

    def generate_all(self, activity, sax_string, classNo):
        # Move up the sax_string by some 'shift' amount, each image will have some portion of the previous image within it.
        shift = 100
        for i in range(0, len(sax_string), shift):
            counter = i // shift

            # 1 in 5 images generated get placed into the test set. This ensures we have a train/test breakdown of:
            # 80% / 20% for train and test respectively.
            if i % (shift * 5) != 0:
                self.generate(activity, sax_string, classNo, counter, shift, 'train')
            else:
                self.generate(activity, sax_string, classNo, counter, shift, 'test')

    def generate(self, activity, sax_string, classNo, counter, shift, data_group):
        # Image size: 32x32
        image = Bitmap(self.bitmap_size, self.bitmap_size)
        
        # Try and Except - Except needed when iterations extend passed the SAX string length. 
        try:
            for row in range(self.bitmap_size):
                for col in range(self.bitmap_size):
                    # We set each pixel in the bitmap based on the mapping function, from the bitmap_module.
                    letter_choice = (shift * counter) + (row * self.bitmap_size) + col
                    rgb_colour = letter_to_colour(sax_string[letter_choice])
                    image.setPixel(row, col, rgb_colour)

            # Finally, write the bitmaps to the correct location (train/test)
            image.write('./pixel_bitmaps/' + data_group + '/' + activity + '/' + activity + '(' + str(classNo) + ')-image-' + str(counter) + '.bmp')
        except:
            pass


def main():
    generator = BitmapGenerator()
    generator.generate_bitmaps()

if __name__ == "__main__":
    main()

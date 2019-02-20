from symbolic_aggregate_approximation import SymbolicAggregateApproximation
from bitmap_module.letter_to_colour_conversion import letter_to_colour
from bitmap_module.text_to_bmp_class import Bitmap

class BitmapGenerator:

    def __init__(self):
        self.sax_obj = SymbolicAggregateApproximation()

    def generate_bitmaps(self):
        for index in range(1, 7):
            try:
                print("Activity level: " + str(index))
                bitmap_size = 64

                walk_sax_str = self.sax_obj.generate_walk(index)
                self.generate_all("Walk", walk_sax_str, index, bitmap_size)

                run_sax_str = self.sax_obj.generate_run(index)
                self.generate_all("Run", run_sax_str, index, bitmap_size)

                low_bike_sax_str = self.sax_obj.generate_low_bike(index)
                self.generate_all("LowResistanceBike", low_bike_sax_str, index, bitmap_size)

                high_bike_sax_str = self.sax_obj.generate_high_bike(index)
                self.generate_all("HighResistanceBike", high_bike_sax_str, index, bitmap_size)

            except FileNotFoundError:
                print("File not found with ID: (" + str(index) + ")")

    def generate_all(self, activity, sax_string, classNo, size):
        scale = 200
        for i in range(0, len(sax_string), scale):
            counter = i // scale
            self.generate(i, activity, sax_string, classNo, size, counter, scale)

    @staticmethod
    def generate(start_index, activity, sax_string, classNo, size, counter, scale):
        b = Bitmap(size, size)
        try:
            for row in range(size):
                for col in range(size):
                    letter_choice = (scale * counter) + (row * size) + col
                    rgb_colour = letter_to_colour(sax_string[letter_choice])
                    b.setPixel(row, col, rgb_colour)
            b.write('./pixel_bitmaps/train/' + activity + '/' + activity + '(' + str(classNo) + ')-image-' + str(counter) + '.bmp')
        except:
            pass


def main():
    generator = BitmapGenerator()
    generator.generate_bitmaps()

if __name__ == "__main__":
    main()

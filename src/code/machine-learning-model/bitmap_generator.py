from symbolic_aggregate_approximation import SymbolicAggregateApproximation
import text_to_image

class BitmapGenerator:

    def __init__(self):
        self.sax_obj = SymbolicAggregateApproximation()
        self.generate_bitmaps()

    def generate_bitmaps(self):
        try:
            for index in range(1, 7):
                walk_sax_str = self.sax_obj.generate_walk(index)
                self.generate("Walk", walk_sax_str)

                run_sax_str = self.sax_obj.generate_run(index)
                self.generate("Run", run_sax_str)

                low_bike_sax_str = self.sax_obj.generate_low_bike(index)
                self.generate("LowResistanceBike", low_bike_sax_str)

                high_bike_sax_str = self.sax_obj.generate_high_bike(index)
                self.generate("HighResistanceBike", high_bike_sax_str)

        except FileNotFoundError:
            print("File not found")

    @staticmethod
    def generate(activity, activity_sax_repr):
        count = 1
        for i in range(0, len(activity_sax_repr)//32, 1):
            image_source = activity_sax_repr[32*i:32*(i+1)]
            print("Image Letter Scheme #" + str(count) + ": " + image_source)
            text_to_image.encode(image_source, "./pixel_bitmaps/train/" + activity + "/"
                                 + activity + "0" + str(count) + ".png")
            count += 1

def main():
    generator = BitmapGenerator()
    generator.generate_bitmaps()

if __name__ == "__main__":
    main()

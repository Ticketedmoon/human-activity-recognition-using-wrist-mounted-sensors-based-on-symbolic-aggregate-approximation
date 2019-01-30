from symbolic_aggregate_approximation import SymbolicAggregateApproximation
import text_to_image

class BitmapGenerator:

    def __init__(self):
        self.sax_obj = SymbolicAggregateApproximation()

    def generate_bitmaps(self):
        for index in range(1, 7):
            try:
                walk_sax_str = self.sax_obj.generate_walk(index)
                self.generate("Walk", walk_sax_str, index)

                run_sax_str = self.sax_obj.generate_run(index)
                self.generate("Run", run_sax_str, index)

                low_bike_sax_str = self.sax_obj.generate_low_bike(index)
                self.generate("LowResistanceBike", low_bike_sax_str, index)

                high_bike_sax_str = self.sax_obj.generate_high_bike(index)
                self.generate("HighResistanceBike", high_bike_sax_str, index)

            except FileNotFoundError:
                print("File not found with ID: (" + str(index) + ")")

    @staticmethod
    def generate(activity, activity_sax_repr, classNo):
        count = 1
        for i in range(0, len(activity_sax_repr)//64, 1):
            image_source = activity_sax_repr[64*i:64*(i+1)]
            print("image class: (" + str(classNo) + ") Activity: (" + activity + ") Representation" + ": " + image_source)
            if i % 5 == 0:
                text_to_image.encode(image_source, "./pixel_bitmaps/test/" + activity + "/"
                                    + activity + "0" + str(classNo) + "-" + str(count) + ".png")
            else:
                text_to_image.encode(image_source, "./pixel_bitmaps/train/" + activity + "/"
                                    + activity + "0" + str(classNo) + "-" + str(count) + ".png")
            count += 1

def main():
    generator = BitmapGenerator()
    generator.generate_bitmaps()

if __name__ == "__main__":
    main()

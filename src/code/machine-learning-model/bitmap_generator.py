from sax_transformation import Sax
import text_to_image


class BitmapGenerator:

    bitmap_strings = []

    def __init__(self):
        self.sax_transform = Sax()
        self.build_bitmap_strings()

    def build_bitmap_strings(self):
        walk_str, run_str = self.sax_transform.apply_sax_transformation()
        self.bitmap_strings.append(walk_str)
        self.bitmap_strings.append(run_str)

    def generate_bitmaps(self):
        count = 0
        for activity_string in self.bitmap_strings:
            print(activity_string)
            for i in range(0, len(activity_string)//32, 1):
                image_source = activity_string[32*i:32*(i+1)]
                print("Image Letter Scheme #" + str(count) + ": " + image_source)
                text_to_image.encode(image_source, "./pixel_bitmaps/activity" + str(count) + ".png")
                count += 1

    

def main():
    generator = BitmapGenerator()
    generator.generate_bitmaps()


if __name__ == "__main__":
    main()

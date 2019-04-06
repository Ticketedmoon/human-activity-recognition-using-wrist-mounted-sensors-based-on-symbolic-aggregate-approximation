# This script's purpose is to ensure each class of data will have an equal amount.
import os
import re
from logger_module.Logger import Logger

logger = Logger()

path, dirs, files = next(os.walk("./pixel_bitmaps/train/HighResistanceBike"))
file_count = len(files)
print("Limiting all training directories to size: " + str(file_count))

folder_walk = './pixel_bitmaps/train/Walk'
folder_run = './pixel_bitmaps/train/Run'
folder_low_resistance_bike = './pixel_bitmaps/train/LowResistanceBike'

def limit_to_folder_size(folder):
    for the_file in os.listdir(folder):
        p = re.compile(r'\d+')
        picture_id = (int) (''.join(p.findall(the_file)))
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path) and picture_id > file_count:
                os.unlink(file_path)
        except Exception as e:
            logger.error("Problem limiting folder to correct size...")

if __name__ == "__main__":
    limit_to_folder_size(folder_walk)
    limit_to_folder_size(folder_run)
    limit_to_folder_size(folder_low_resistance_bike)
    logger.info("Directory reshape complete.")
# This script's purpose is to ensure each class of data will have an equal amount.
import os
import re
import sys

sys.path.append("../")
from logger_module.Logger import Logger

logger = Logger("../", "logs/Machine_Learning")

def limit_to_folder_size(mode):

    path, dirs, files = next(os.walk("./pixel_bitmaps/{}/HighResistanceBike".format(mode)))
    file_count = len(files)
    logger.info("Limiting all {} directories to size: {}".format(mode, file_count))

    folder_walk = './pixel_bitmaps/{}/Walk'.format(mode)
    folder_run = './pixel_bitmaps/{}/Run'.format(mode)
    folder_low_resistance_bike = './pixel_bitmaps/{}/LowResistanceBike'.format(mode)
    folders = [folder_walk, folder_run, folder_low_resistance_bike]

    for folder in folders:
        for the_file in os.listdir(folder):
            if (the_file != ".gitkeep"):
                p = re.compile(r'\d+')
                picture_id = (int) (''.join(p.findall(the_file)))
                file_path = os.path.join(folder, the_file)
                try:
                    if os.path.isfile(file_path) and picture_id > file_count:
                        os.unlink(file_path)
                except Exception as e:
                    logger.error("Problem limiting folder to correct size...")

if __name__ == "__main__":
    mode = sys.argv[1]
    if (mode)
    limit_to_folder_size(mode)
    logger.info("Directory reshape complete.")

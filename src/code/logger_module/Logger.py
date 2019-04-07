import logging

class Logger:

    filepath = 'logger_module/'
    filemode = 'w'

    def __init__(self, path, filename):
        logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s', level=logging.INFO,
                            handlers=[
                                logging.FileHandler("{0}/{1}.log".format(path + self.filepath, filename)),
                                logging.StreamHandler()
                            ])

    def warning(self, message):
        logging.warning(message)

    def info(self, message):
        logging.info(message)

    def debug(self, message):
        logging.debug(message)

    def error(self, message):
        logging.error(message)
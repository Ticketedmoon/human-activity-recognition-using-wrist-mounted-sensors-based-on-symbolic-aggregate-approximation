import logging

class Logger:

    filepath = 'logger_module/'
    filemode = 'w'

    def __init__(self, path, filename, testMode=False):
        logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s', level=logging.INFO,
                            handlers=[
                                logging.FileHandler("{0}/{1}.log".format(path + self.filepath, filename)),
                                logging.StreamHandler()
                            ])
        self.testMode = testMode
        self.logger_path = path

    def warning(self, message):
        if(not self.testMode):
            logging.warning(message)

    def info(self, message):
        if(not self.testMode):
            logging.info(message)

    def debug(self, message):
        if(not self.testMode):
            logging.debug(message)

    def error(self, message):
        if(not self.testMode):
            logging.error(message)
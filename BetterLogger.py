import logging
import sys

class BetterLogger():
    def __init__(self, logger_name):
        """
        Initializes a logger that outputs to a file, as well
        as to the console
        """
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s UTC - %(levelname)s - %(message)s")

        # log to the console
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)
        stdout_handler.setFormatter(formatter)

        # log to a file
        file_handler = logging.FileHandler(filename="log.txt")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        self.logger.addHandler(stdout_handler)
        self.logger.addHandler(file_handler)

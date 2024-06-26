import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s UTC - %(levelname)s - %(message)s")

# log to the console
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)

# log to a file
file_handler = logging.FileHandler(filename="log.txt")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(stdout_handler)
logger.addHandler(file_handler)

COLOR_RED = "\x1b[31m"
COLOR_GREEN = "\x1b[32m"
COLOR_YELLOW = "\x1b[33m"
COLOR_BLUE = "\x1b[34m"
COLOR_PINK = "\x1b[38;5;201m"
COLOR_END = "\x1b[0m"

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

COLOR_GREEN = '\033[92m'
COLOR_BLUE = '\033[94m'
COLOR_ORANGE = '\033[93m'
COLOR_RED = '\033[91m'
COLOR_END = '\033[0m'

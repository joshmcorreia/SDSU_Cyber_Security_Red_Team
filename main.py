import yaml
from BetterLogger import logger


def read_config_file():
    logger.debug("Reading config file...")
    with open("config.yaml", "r") as file_in:
        parsed_config = yaml.safe_load(file_in)
    logger.debug("Successfully read config file")
    return parsed_config

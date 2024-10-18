# Standard imports
import logging
import logging.config

# Related third party imports

# Local application/library specific imports


SCHEMAS_PATH = "schemas/"
RULES_PATH = "rules/"
DATA_PATH = "data/"
OUTPUT_PATH = "output/"


def setup_logging():
    logging.config.fileConfig("profiler/logging.conf")
    return logging.getLogger("root")

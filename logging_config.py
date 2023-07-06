# logging_config.py
import logging
import os

def configure_logging(log_level=logging.INFO, log_file=None):
    # Create a basic logging configuration
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler()
        ]
    )

    # If a log file is specified, add a FileHandler to the logging configuration
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"))
        logging.getLogger().addHandler(file_handler)
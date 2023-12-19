import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging():
    # Create the root logger
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    # Check if the log file exists and get the path 
    log_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", 'logs.txt')
    if not os.path.exists(log_file_path):
        with open(log_file_path, 'w') as f:
            f.write("")

    # Optionally, add a file handler for writing logs to a file
    file_handler = RotatingFileHandler(log_file_path, maxBytes=1e6, backupCount=5)
    file_handler.setLevel(logging.DEBUG) # Lowest, captures every log message
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_handler)
    return logging.getLogger()

# You can add more configuration options as needed

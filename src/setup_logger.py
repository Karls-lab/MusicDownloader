import logging
from logging.handlers import RotatingFileHandler

def setup_logging(log_file="app.log"):
    # Create the root logger
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    # Optionally, add a file handler for writing logs to a file
    file_handler = RotatingFileHandler(log_file, maxBytes=1e6, backupCount=5)
    file_handler.setLevel(logging.DEBUG) # Lowest, captures every log message
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_handler)
    return logging.getLogger()

# You can add more configuration options as needed

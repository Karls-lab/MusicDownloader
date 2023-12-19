from model import Model
from view import View
from controller import Controller
import setup_logger
import sys


if __name__ == "__main__":
    logger = setup_logger.setup_logging()

    if logger is None:
        sys.exit()

    model = Model(logger)
    view = View(None) 
    view.controller = Controller(model, view)
    view.setupView()
    


#!/usr/bin/env python3

from src.model import Model
from src.view import View
from src.controller import Controller
from src import setup_logger


if __name__ == "__main__":
    logger = setup_logger.setup_logging()
    if logger is None:
        print("ERROR, Logger not setup correctly")

    model = Model(logger)
    view = View(logger, None) 
    view.controller = Controller(logger, model, view)
    view.setupView()
    


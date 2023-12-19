#!/usr/bin/env python3

from src.model import Model
from src.view import View
from src.controller import Controller
from src import setup_logger
import sys


if __name__ == "__main__":
    logger = setup_logger.setup_logging()

    if logger is None:
        sys.exit()

    model = Model(logger)
    view = View(None) 
    view.controller = Controller(model, view)
    view.setupView()
    


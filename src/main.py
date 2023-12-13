from model import Model
from view import View
from controller import Controller
import tkinter as tk


if __name__ == "__main__":
    model = Model()
    view = View(None) 
    view.controller = Controller(model, view)
    view.setupView()

import tkinter as tk
import numpy as np
from listener import Listener


class App(tk.Frame):
    WINDOW_VARS = {"window": False, "canvas": False, "stream": False, "audioData": np.array([])}  # reference to window
    WIDTH = 600
    HEIGHT = 400
    TIMEOUT = 10

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

        self.listener = Listener(self.WINDOW_VARS)
        self.add_ui_elements()

    def add_ui_elements(self):
        self.add_canvas()
        self.add_listen_btns()

    def add_canvas(self):
        self.canvas = tk.Canvas(self, width=self.WIDTH, height=self.HEIGHT)
        self.canvas.pack(side="top")
        self.WINDOW_VARS["canvas"] = self.canvas

    def add_listen_btns(self):
        listen_btn = tk.Button(self, text="Listen", command=self.listener.listen)
        listen_btn.pack(side="bottom")
        stop_btn = tk.Button(self, text="Stop", command=self.listener.stop)
        stop_btn.pack(side="bottom")
        return

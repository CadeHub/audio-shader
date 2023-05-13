import PySimpleGUI as gui
from listener import Listener


class GUI:
    WINDOW_VARS = {"window": False}  # reference to window

    def __init__(self):
        AppFont = "Any 16"
        gui.theme("DarkTeal3")

        layout = [
            [gui.ProgressBar(10000, orientation="h", size=(20, 20), key="-PROG-")],
            [gui.Button("Listen", font=AppFont), gui.Button("Exit", font=AppFont)],
        ]

        self.WINDOW_VARS["window"] = gui.Window("Mic Max Data", layout, finalize=True)
        self.create_listener()

    def create_listener(self):
        self.LISTENER = Listener(self.WINDOW_VARS)

    def launch_gui(self):
        while True:
            event, values = self.WINDOW_VARS["window"].read()
            if event == gui.WIN_CLOSED or event == "Exit":
                self.close()
                return
            if event == "Listen":
                self.LISTENER.listen()

    def close(self):
        self.WINDOW_VARS["window"].close()
        return

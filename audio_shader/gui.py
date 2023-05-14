import numpy as np
import PySimpleGUI as gui
from listener import Listener


class GUI:
    WINDOW_VARS = {"window": False, "stream": False, "audioData": np.array([])}  # reference to window
    TIMEOUT = 10

    def __init__(self):
        self.init_gui()
        self.create_listener()

    def init_gui(self):
        AppFont = "Any 16"
        gui.theme("DarkTeal3")

        layout = [
            [
                gui.Graph(
                    canvas_size=(500, 500),
                    graph_bottom_left=(-2, -2),
                    graph_top_right=(102, 102),
                    background_color="#809AB6",
                    key="graph",
                )
            ],
            [gui.ProgressBar(4000, orientation="h", size=(20, 20), key="-PROG-")],
            [
                gui.Button("Listen", font=AppFont),
                gui.Button("Stop", font=AppFont, disabled=True),
                gui.Button("Exit", font=AppFont),
            ],
        ]

        self.WINDOW_VARS["window"] = gui.Window("Audio Visualizer", layout, finalize=True)
        self.graph = self.WINDOW_VARS["window"]["graph"]
        self.drawAxis()
        return

    def create_listener(self):
        self.LISTENER = Listener(self.WINDOW_VARS)

    def launch_gui(self):
        while True:
            event, values = self.WINDOW_VARS["window"].read(timeout=self.TIMEOUT)
            if event == gui.WIN_CLOSED or event == "Exit":
                self.close()
                return
            if event == "Listen":
                self.LISTENER.listen()
            if event == "Stop":
                self.LISTENER.stop()

            elif self.WINDOW_VARS["audioData"].size != 0:
                # Uodate volumne meter
                self.WINDOW_VARS["window"]["-PROG-"].update(np.amax(self.WINDOW_VARS["audioData"]))
                # Redraw plot
                self.graph.erase()
                self.drawAxis()

                # Here we go through the points in the audioData object and draw them
                # Note that we are rescaling ( dividing by 100 ) and centering (+50 )
                # try different values to get a feel for what they do.

                for x in range(self.LISTENER.CHUNK):
                    self.graph.DrawCircle(
                        (x, (self.WINDOW_VARS["audioData"][x] / 100) + 50), 0.4, line_color="blue", fill_color="blue"
                    )

    def drawAxis(self, dataRangeMin=0, dataRangeMax=100):
        # Y Axis
        self.graph.DrawLine((0, 50), (100, 50))
        # X Axis
        self.graph.DrawLine((0, dataRangeMin), (0, dataRangeMax))

    def close(self):
        if self.WINDOW_VARS["stream"]:
            self.WINDOW_VARS["stream"].stop_stream()
            self.WINDOW_VARS["stream"].close()
            self.WINDOW_VARS["window"]["-PROG-"].update(0)
        self.WINDOW_VARS["window"].close()
        return

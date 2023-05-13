import numpy as np
import pyaudio


class Listener:
    def __init__(self, WINDOW_VARS=None):
        self.CHUNK = 1024
        self.RATE = 44100
        self.INTERVAL = 4
        self.WINDOW_VARS = WINDOW_VARS

    def listen_callback(self, in_data, frame_count, time_info, status):
        self.WINDOW_VARS["audioData"] = np.frombuffer(in_data, dtype=np.int16)

        # self.WINDOW_VARS["window"]["-PROG-"].update(np.amax(data))
        return (in_data, pyaudio.paContinue)

    def listen(self):
        p = pyaudio.PyAudio()
        self.WINDOW_VARS["stream"] = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK,
            stream_callback=self.listen_callback,
        )

        self.WINDOW_VARS["stream"].start_stream()
        self.WINDOW_VARS["window"]["Stop"].Update(disabled=False)
        self.WINDOW_VARS["window"]["Listen"].Update(disabled=True)

    def stop(self):
        if self.WINDOW_VARS["stream"]:
            self.WINDOW_VARS["stream"].stop_stream()
            self.WINDOW_VARS["stream"].close()
            self.WINDOW_VARS["window"]["-PROG-"].update(0)
            self.WINDOW_VARS["window"]["Stop"].Update(disabled=True)
            self.WINDOW_VARS["window"]["Listen"].Update(disabled=False)

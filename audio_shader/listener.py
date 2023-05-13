import numpy as np
import pyaudio


class Listener:
    def __init__(self, WINDOW_VARS=None):
        self.CHUNK = 1024
        self.RATE = 44100
        self.INTERVAL = 4
        self.WINDOW_VARS = WINDOW_VARS

    def listen(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)

        # Loop through chunks:
        for i in range(int(self.INTERVAL * self.RATE / self.CHUNK)):
            data = np.frombuffer(stream.read(self.CHUNK), dtype=np.int16)
            chunkMax = np.amax(data)
            # print(chunkMax)
            # Update the progressBar via the window reference.
            self.WINDOW_VARS["window"]["-PROG-"].update(chunkMax)
        # reset the progress bar after listening.
        self.WINDOW_VARS["window"]["-PROG-"].update(0)

        # Tidy up, this time this code runs:
        stream.stop_stream()
        stream.close()
        print("closing stream")
        p.terminate()
        print("terminating PyAudio")

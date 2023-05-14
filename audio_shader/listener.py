import numpy as np
import pyaudio


class Listener:
    VERTICES = 3

    def __init__(self, WINDOW_VARS=None):
        self.CHUNK = 1024
        self.RATE = 44100
        self.INTERVAL = 3
        self.WINDOW_VARS = WINDOW_VARS

    def listen_callback(self, in_data, frame_count, time_info, status):
        self.WINDOW_VARS["audioData"] = np.frombuffer(in_data, dtype=np.int16)


        self.draw_triangle(np.fromstring(in_data, dtype=np.int16))

        return (in_data, pyaudio.paContinue)

    def draw_shape(self, data):
        self.WINDOW_VARS["canvas"].delete("all")

        # process data
        data = np.fromstring(data, dtype=np.int16)
        matrix = np.random.choice(data, ((self.VERTICES - 1) * 4))
        # print(matrix)

        self.WINDOW_VARS["canvas"].create_line(matrix[i][0], matrix[i][1], matrix[i][2], matrix[i][3], fill="green", width=5)


        # testing
        # tmp = int(np.amax(data)) / 10
        # self.WINDOW_VARS["canvas"].create_rectangle((150-(abs(tmp))), (100-(abs(tmp))), (150+(abs(tmp))), (100+(abs(tmp))), fill="pink")
        return
    
    def draw_triangle(self, data):
        self.WINDOW_VARS["canvas"].delete("all")

        # process data
        data = np.fromstring(data, dtype=np.int16)
        vals = np.random.choice(data, 3)

        # temp
        v1 = Vertex(300, 300 - abs(vals[0]))
        v2 = Vertex(300 + abs(vals[1]), 300)
        v3 = Vertex(300 - abs(vals[2]), 300)

        # draw cener line
        self.WINDOW_VARS["canvas"].create_line(300, 300, 300, v1.y, fill="blue", width=3)

        self.WINDOW_VARS["canvas"].create_line(v1.x, v1.y, v2.x, v2.y, fill="green", width=5)
        self.WINDOW_VARS["canvas"].create_line(v1.x, v1.y, v3.x, v3.y, fill="pink", width=5)
        self.WINDOW_VARS["canvas"].create_line(v2.x, v2.y, v3.x, v3.y, fill="red", width=5)

        # self.WINDOW_VARS["canvas"].create_line(matrix[i][0], matrix[i][1], matrix[i][2], matrix[i][3], fill="green", width=5)
        return

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

    def stop(self):
        if self.WINDOW_VARS["stream"]:
            self.WINDOW_VARS["stream"].stop_stream()
            self.WINDOW_VARS["stream"].close()


class Vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y
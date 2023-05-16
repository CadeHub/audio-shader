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

        # self.draw_triangle(np.fromstring(in_data, dtype=np.int16))
        self.draw_polygon(np.fromstring(in_data, dtype=np.int16))
        # self.draw_oval(np.fromstring(in_data, dtype=np.int16))

        return (in_data, pyaudio.paContinue)

    def draw_shape(self, data):
        self.WINDOW_VARS["canvas"].delete("all")

        # process data
        data = np.fromstring(data, dtype=np.int16)
        np.random.choice(data, ((self.VERTICES - 1) * 4))
        # print(matrix)

        # self.WINDOW_VARS["canvas"].create_line(
        #     matrix[i][0], matrix[i][1], matrix[i][2], matrix[i][3], fill="green", width=5
        # )

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
        v3 = Vertex(300 - abs(vals[1]), 300)
        v4 = Vertex(300, 300 + abs(vals[0]))

        # draw cener line
        self.WINDOW_VARS["canvas"].create_line(300, v4.y, 300, v1.y, fill="black", width=3)
        self.WINDOW_VARS["canvas"].create_line(v2.x, v2.y, v3.x, v3.y, fill="white", width=3)

        self.WINDOW_VARS["canvas"].create_line(v1.x, v1.y, v2.x, v2.y, fill="grey", width=5)
        self.WINDOW_VARS["canvas"].create_line(v1.x, v1.y, v3.x, v3.y, fill="grey", width=5)

        self.WINDOW_VARS["canvas"].create_line(v4.x, v4.y, v3.x, v3.y, fill="grey", width=5)
        self.WINDOW_VARS["canvas"].create_line(v4.x, v4.y, v2.x, v2.y, fill="grey", width=5)
        return

    def draw_polygon(self, data):
        self.WINDOW_VARS["canvas"].delete("all")
        data = np.fromstring(data, dtype=np.int16)

        val = np.amax(data)
        print(val)

        x_val = abs(val) / 200
        y_val = abs(val) / 200

        print(f"{x_val}, {y_val}")

        center_x = 300
        center_y = 200

        c = Vertex(center_x, center_y)

        l = Vertex(center_x - x_val, center_y)
        r = Vertex(center_x + x_val, center_y)

        t = Vertex(center_x, center_y - y_val)
        b = Vertex(center_x, center_y + y_val)

        self.WINDOW_VARS["canvas"].create_polygon(c.x, c.y, t.x, t.y, r.x, r.y)  # right angle tri
        self.WINDOW_VARS["canvas"].create_polygon(c.x, c.y, t.x, t.y, l.x, l.y, fill="black")  # left angle tri

        self.WINDOW_VARS["canvas"].create_polygon(c.x, c.y, b.x, b.y, r.x, r.y, fill="black")  # right angle tri
        self.WINDOW_VARS["canvas"].create_polygon(c.x, c.y, b.x, b.y, l.x, l.y)  # left angle tri

        return

    def draw_oval(self, data):
        self.WINDOW_VARS["canvas"].delete("all")
        data = np.fromstring(data, dtype=np.int16)

        val = np.amax(data)
        radius = abs(val) / 100

        center_x = 300
        center_y = 200
        c = Vertex(center_x, center_y)

        color = self.generate_color(data)

        self.draw_circle(c.x, c.y, radius, color)
        return

    def draw_circle(self, x, y, r, color="RED"):
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        return self.WINDOW_VARS["canvas"].create_oval(x0, y0, x1, y1, fill=color)

    def generate_color(self, data):
        str = "#"
        hex_vals = np.random.choice(data, 3)

        for val in hex_vals:
            tmp = f"{abs(val)}"
            tmp = f"{hex(int(tmp))}"[2:]
            tmp = tmp[0:2] if len(tmp) >= 2 else f"0{tmp}"
            str += tmp

        return str

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

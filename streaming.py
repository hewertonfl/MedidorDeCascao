import asyncio
import base64
import dash
import cv2
import dash_html_components as html
import threading

from dash.dependencies import Output, Input
from quart import Quart, websocket
from dash_extensions import WebSocket


class VideoCamera(object):
    def __init__(self, video_path):
        self.video = cv2.VideoCapture(video_path)

    def __del__(self):
        self.video.release()

    def get_frame(self):

        success, image = self.video.read()

        # Recolor image to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


# Setup small Quart server for streaming via websocket, one for each stream.
server = Quart(__name__)
n_streams = 1


async def stream(camera, delay=None):
    while True:
        if delay is not None:
            await asyncio.sleep(delay)  # add delay if CPU usage is too high
        frame = camera.get_frame()
        await websocket.send(f"data:image/jpeg;base64, {base64.b64encode(frame).decode()}")


@server.websocket("/stream0")
async def stream0():
    camera = VideoCamera(0)
    await stream(camera)


@server.websocket("/stream1")
async def stream1():
    camera = VideoCamera('rtsp://192.168.100.43:8080/h264_ulaw.sdp')
    await stream(camera)


# Create small Dash application for UI.
app = dash.Dash(__name__)
app.layout = html.Div(
    [html.Img(style={'width': '40%', 'padding': 10}, id=f"v{i}") for i in range(n_streams)] +
    [WebSocket(
        url=f"ws://127.0.0.1:5000/stream{i}", id=f"ws{i}") for i in range(n_streams)]
)
# Copy data from websockets to Img elements.
for i in range(n_streams):
    app.clientside_callback("function(m){return m? m.data : '';}", Output(
        f"v{i}", "src"), Input(f"ws{i}", "message"))

if __name__ == '__main__':
    threading.Thread(target=app.run_server).start()
    server.run()

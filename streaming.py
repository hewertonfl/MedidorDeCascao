import asyncio
import base64
import dash
import cv2
import numpy as np

from dash.dependencies import Output, Input
from quart import Quart, websocket
from dash_extensions import WebSocket
from ultralytics import YOLO

model = YOLO('C:\\Users\\hewer\\OneDrive\\Área de Trabalho\\Medidor de cascão\\video_cascao\\best.pt') 
class VideoCamera(object):
    def __init__(self, video_path):
        self.video = cv2.VideoCapture(video_path)

    def __del__(self):
        self.video.release()

    def calc_greater_distance(self,polygon):
        greater_distance = 0
        for point1 in polygon:
            for point2 in polygon:
                if point1[0][1] == point2[0][1] and abs(point1[0][0] - point2[0][0]) > greater_distance:
                    greater_distance = abs(point1[0][0] - point2[0][0])
                    p1=point1[0][0],point1[0][1]
                    p2=point2[0][0],point2[0][1]
        return p1,p2,greater_distance

    def get_frame(self):

        success, image = self.video.read()

        results = model(image,stream=True,verbose=False)
        for result in results:
            try:
              mask=result[0].masks.xy
              mask = np.array(mask, np.int32)
              mask = mask.reshape((-1,1,2))
              annotated_frame =cv2.polylines(result.plot(boxes=False,masks=True),[mask],True,(0,255,255))

              # Cálculo dos pontos e distância entre os pontos
              p1,p2,d = self.calc_greater_distance(mask)
              position= p1[0],p1[1]-10
              distancia = str(d) +" mm"

              annotated_frame = cv2.line(annotated_frame, p2,p1, (0, 255, 0) ,9)
              annotated_frame = cv2.putText(annotated_frame, distancia, position ,cv2.FONT_HERSHEY_SIMPLEX,1,(0, 255, 0),3,cv2.LINE_AA )
            except Exception as e:
                print(e)
                pass
        #annotated_frame = results[0].plot()

        _, jpeg = cv2.imencode('.jpg', annotated_frame)
        return jpeg.tobytes()


# Setup small Quart server for streaming via websocket, one for each stream.
server = Quart(__name__)

async def stream(camera, delay=None):
    while True:
        if delay is not None:
            await asyncio.sleep(delay)  # add delay if CPU usage is too high
        frame = camera.get_frame()
        await websocket.send(f"data:image/jpeg;base64, {base64.b64encode(frame).decode()}")


@server.websocket("/stream0")
async def stream0():
    camera = VideoCamera("C:\\Users\\hewer\\OneDrive\\Área de Trabalho\\Medidor de cascão\\video_cascao\\CortadoDSC_0005.mp4")
    await stream(camera)


# @server.websocket("/stream1")
# async def stream1():
#     camera = VideoCamera('rtsp://192.168.100.43:8080/h264_ulaw.sdp')
#     await stream(camera)

if __name__ == '__main__':
    server.run()
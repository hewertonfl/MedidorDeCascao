import asyncio
import base64
import dash
import cv2
import numpy as np

from dash.dependencies import Output, Input
from quart import Quart, websocket
from dash_extensions import WebSocket
from ultralytics import YOLO

from customDataframe import *
from datetime import datetime

model = YOLO('./yolov8n-seg.pt') 
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
        annotated_frame = image
        # Parâmetros de redimensionamento
        scale_percent = 50
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)
        image = cv2.resize(image,dim,interpolation = cv2.INTER_AREA)
        annotated_frame = image

        results = model(image,device=0,stream=True,verbose=False)
        for result in results:
            try:
                #Obtenção das mascaras
                mask=result[0].masks.xy
                mask = np.array(mask, np.int32)
                mask = mask.reshape((-1,1,2))
            # annotated_frame =cv2.polylines(result.plot(boxes=False,masks=True),[mask],True,(0,255,255))
                annotated_frame =cv2.polylines(image,[mask],True,(0,255,255),5)

                # Cálculo dos pontos e distância entre os pontos
                p1,p2,d = self.calc_greater_distance(mask)
                position= p1[0],p1[1]-10
                d= int(d*0.6)
                distancia = str(d) +" mm"

                # Obtenção do tempo
                currentTime = datetime.now().strftime("%H:%M:%S")
                create_dataframe(currentTime,d)

                annotated_frame = cv2.line(annotated_frame, p2,p1, (0, 255, 0) ,9)
                annotated_frame = cv2.putText(annotated_frame, distancia, position ,cv2.FONT_HERSHEY_SIMPLEX,1,(0, 255, 0),3,cv2.LINE_AA )
                
            except Exception as e:
                print("Erro no try: ", e)
                pass

        _, jpeg = cv2.imencode('.jpg', annotated_frame)
        return jpeg.tobytes()

server = Quart(__name__)

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

if __name__ == '__main__':
    server.run()
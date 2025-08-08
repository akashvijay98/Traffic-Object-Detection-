import cv2
import torch
import os

import boto3


print("Current working directory:", os.getcwd())
model = None

def load_model():
    global model
    if model is None:
        model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

def process_video(input_video_path: str, output_video_path: str):
    load_model()
    cap = cv2.VideoCapture(input_video_path)

    if not cap.isOpened():
        raise RuntimeError("Could not open input video")

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        results.render()
        out.write(results.ims[0])  # Annotated frame

    cap.release()
    out.release()

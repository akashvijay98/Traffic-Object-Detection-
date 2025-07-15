import cv2
import torch

import os
print("Current working directory:", os.getcwd())

# Load YOLOv5 model (pretrained on COCO)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Open video file
video_path = 'C:/Users/ajayv/PycharmProjects/Traffic-Object-Detection-/traffic_detection/data/video.mp4'
cap = cv2.VideoCapture(video_path)

# Read the first frame to get width and height
ret, frame = cap.read()
if not ret:
    print("Failed to read the video")
    cap.release()
    exit()
else:
    print("Video opened successfully, first frame read.")
    print(f"Frame shape: {frame.shape}")

height, width = frame.shape[:2]

# Setup video writer with the correct size
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_with_boxes.mp4', fourcc, 20.0, (width, height))

while True:
    # Run inference on the current frame
    results = model(frame)

    # Render boxes and labels onto frame (in-place)
    results.render()
    output_frame = results.ims[0]  # This is a numpy array (H, W, 3) with boxes

    # Write the frame with detections
    out.write(output_frame)

    # Display the frame
    cv2.imshow('YOLOv5 Detection', output_frame)

    # Read next frame
    ret, frame = cap.read()
    if not ret:
        break

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()

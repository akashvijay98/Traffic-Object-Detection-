from fastapi import FastAPI, UploadFile, File
import sys
import os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
print("sys.path append:", ROOT_DIR)
sys.path.append(ROOT_DIR)


import uuid
from .tasks import process_video_task
from .aws_util import upload_to_s3_from_bytes, download_from_s3

from traffic_detection.script.detect_objects_yolo import process_video


app = FastAPI()

INPUT_BUCKET = "avijay48inputfiles"
OUTPUT_BUCKET = "avijay48outputfiles"
TEMP_DIR = "temp"

os.makedirs(TEMP_DIR, exist_ok=True)


@app.post("/process-video/")
async def process_video_api(file: UploadFile = File(...)):
    # generate a unique file id
    file_id = str(uuid.uuid4())
    filename = f"{file_id}_{file.filename}"

    print("filename:", filename)

    # In-memory approach to avoid local disk writes in the API
    file_contents = await file.read()

    if not upload_to_s3_from_bytes(file_contents, INPUT_BUCKET, filename):
        return {"error": "Failed to upload file to S3"}, 500


    task = process_video_task.apply_async(args=[filename])

    return {
        "message": "File uploaded and processing job has been queued.",
        "input_file": filename,
        "task_id": task.id,
        "output_s3_url": f"s3://{OUTPUT_BUCKET}/processed_{filename}"
    }




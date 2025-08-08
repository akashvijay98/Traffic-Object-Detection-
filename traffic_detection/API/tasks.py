
import os
from .celery_app import app

from .aws_util import download_from_s3, upload_to_s3_from_bytes

from traffic_detection.script.detect_objects_yolo import process_video
INPUT_BUCKET = "avijay48inputfiles"
OUTPUT_BUCKET = "avijay48outputfiles"
TEMP_DIR = "/tmp"

os.makedirs(TEMP_DIR, exist_ok=True)
@app.task(name="process_video_task")
def process_video_task(input_filename: str):
    try:
        print(f"Starting to process video: {input_filename}")
        local_input_path = os.path.join(TEMP_DIR, input_filename)
        download_from_s3(INPUT_BUCKET, input_filename, local_input_path)

        output_filename = f"processed_{input_filename}"
        output_local_path = os.path.join(TEMP_DIR, output_filename)
        process_video(local_input_path, output_local_path)

        # Upload processed video to S3
        with open(output_local_path, 'rb') as f:
            if not upload_to_s3_from_bytes(f.read(), OUTPUT_BUCKET, output_filename):
                raise RuntimeError("Failed to upload processed file to S3")

        os.remove(local_input_path)
        os.remove(output_local_path)

        print(f"Successfully processed {input_filename} and uploaded {output_filename}")

        return {"output_file": output_filename, "status": "success"}

    except Exception as e:
        print(f"Error processing video {input_filename}: {e}")
        return {"error": str(e), "status": "failed"}
import boto3
import os
from botocore.exceptions import ClientError
import logging
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
print("sys.path append:", ROOT_DIR)
sys.path.append(ROOT_DIR)

s3 = boto3.client('s3', region_name='us-east-1')

def upload_to_s3_from_bytes(data: bytes, bucket: str, key: str):
    s3_client = boto3.client('s3')
    try:
        response = s3_client.put_object(
            Bucket=bucket,
            Key=key,
            Body=data
        )
        print(f"Successfully uploaded {key} to S3 bucket {bucket}.")
        return True
    except ClientError as e:
        logging.error(e)
        return False

def download_from_s3(bucket_name, s3_path, local_path):
    s3.download_file(bucket_name, s3_path, local_path)

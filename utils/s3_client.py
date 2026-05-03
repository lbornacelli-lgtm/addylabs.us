import boto3
import sys
sys.path.append('/home/ubuntu/addylabs')
from config.settings import AWS_REGION, S3_MEDIA_BUCKET, S3_ETL_BUCKET, S3_STATIC_BUCKET

s3 = boto3.client("s3", region_name=AWS_REGION)

def upload(file_path, key, bucket=None):
    bucket = bucket or S3_ETL_BUCKET
    s3.upload_file(file_path, bucket, key)
    print(f"Uploaded {file_path} to s3://{bucket}/{key}")

def download(key, file_path, bucket=None):
    bucket = bucket or S3_ETL_BUCKET
    s3.download_file(bucket, key, file_path)
    print(f"Downloaded s3://{bucket}/{key} to {file_path}")

def list_files(prefix="", bucket=None):
    bucket = bucket or S3_ETL_BUCKET
    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    return [obj["Key"] for obj in response.get("Contents", [])]

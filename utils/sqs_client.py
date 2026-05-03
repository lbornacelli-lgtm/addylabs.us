import boto3
import json
import sys
sys.path.append('/home/ubuntu/addylabs')
from config.settings import AWS_REGION, SQS_ETL_QUEUE, SQS_BG_QUEUE

sqs = boto3.client("sqs", region_name=AWS_REGION)

def send_job(payload, queue=None):
    queue = queue or SQS_ETL_QUEUE
    response = sqs.send_message(
        QueueUrl=queue,
        MessageBody=json.dumps(payload)
    )
    print(f"Job sent: {response['MessageId']}")
    return response["MessageId"]

def receive_jobs(max_messages=1, queue=None):
    queue = queue or SQS_ETL_QUEUE
    response = sqs.receive_message(
        QueueUrl=queue,
        MaxNumberOfMessages=max_messages,
        WaitTimeSeconds=5
    )
    return response.get("Messages", [])

def delete_job(receipt_handle, queue=None):
    queue = queue or SQS_ETL_QUEUE
    sqs.delete_message(QueueUrl=queue, ReceiptHandle=receipt_handle)

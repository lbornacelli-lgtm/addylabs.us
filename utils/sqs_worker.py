#!/usr/bin/env python3
# ============================================================
# AddyLabs SQS Worker
# Processes jobs from lawborn-etl-jobs and lawborn-background-jobs
# Run: python3 ~/addylabs/utils/sqs_worker.py
# ============================================================

import sys
import json
import time
import datetime
sys.path.append('/home/ubuntu/addylabs')

from utils.sqs_client import receive_jobs, delete_job, send_job
from utils.mongo_client import insert
from config.settings import SQS_ETL_QUEUE, SQS_BG_QUEUE, LOGS_DIR

def process_job(job):
    body = json.loads(job['Body'])
    job_type = body.get('type')
    payload = body.get('payload', {})
    print(f"[{datetime.datetime.now()}] Processing job: {job_type}")

    if job_type == 'weather_broadcast':
        from agents.weather_agent import generate_weather_broadcast
        result = generate_weather_broadcast()
        insert('weather_broadcasts', {
            'type': 'weather',
            'content': result,
            'timestamp': datetime.datetime.now()
        })
        print("Weather broadcast generated and saved to MongoDB")

    elif job_type == 'tts':
        from agents.tts_agent import speak
        text = payload.get('text', '')
        engine = payload.get('engine', 'piper')
        output = speak(text, engine=engine)
        insert('tts_jobs', {
            'type': 'tts',
            'text': text,
            'engine': engine,
            'output_file': output,
            'timestamp': datetime.datetime.now()
        })
        print(f"TTS audio generated: {output}")

    elif job_type == 'content':
        from agents.content_agent import generate_content
        topic = payload.get('topic', 'General update')
        content_type = payload.get('content_type', 'broadcast')
        result = generate_content(topic, content_type)
        insert('content_jobs', {
            'type': 'content',
            'topic': topic,
            'content': result,
            'timestamp': datetime.datetime.now()
        })
        print("Content generated and saved to MongoDB")

    elif job_type == 'monitor':
        from agents.monitor_agent import run_monitor
        result = run_monitor()
        insert('monitor_reports', {
            'type': 'monitor',
            'report': result,
            'timestamp': datetime.datetime.now()
        })
        print("Monitor report generated and saved to MongoDB")

    else:
        print(f"Unknown job type: {job_type}")

def run_worker(queue=None):
    queue = queue or SQS_ETL_QUEUE
    print(f"[{datetime.datetime.now()}] SQS Worker started — listening on queue...")
    print("Supported job types: weather_broadcast, tts, content, monitor")
    print("Press Ctrl+C to stop\n")

    while True:
        try:
            jobs = receive_jobs(max_messages=5, queue=queue)
            if jobs:
                for job in jobs:
                    try:
                        process_job(job)
                        delete_job(job['ReceiptHandle'], queue=queue)
                        print(f"Job completed and deleted from queue\n")
                    except Exception as e:
                        print(f"Job failed: {e}")
            else:
                print(f"[{datetime.datetime.now()}] No jobs — waiting 10s...")
                time.sleep(10)
        except KeyboardInterrupt:
            print("\nWorker stopped.")
            break

if __name__ == "__main__":
    run_worker()

import os

LITELLM_BASE_URL = "http://localhost:4000"
DEFAULT_AI_MODEL = "claude-sonnet"
DEFAULT_TTS_MODEL = "kokoro-tts"

AWS_REGION = "us-east-1"
S3_MEDIA_BUCKET = "lawborn-media-files"
S3_ETL_BUCKET = "lawborn-etl-data"
S3_STATIC_BUCKET = "lawborn-static-assets"
SQS_ETL_QUEUE = "https://sqs.us-east-1.amazonaws.com/787737883306/lawborn-etl-jobs"
SQS_BG_QUEUE = "https://sqs.us-east-1.amazonaws.com/787737883306/lawborn-background-jobs"

PIPER_URL = "http://localhost:5050"
KOKORO_URL = "http://localhost:5051"
ELEVENLABS_API_KEY = os.environ.get("ELEVEN_API_KEY", "")
ELEVENLABS_VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"

NWS_OFFICE = "JAX"
NWS_ZONE = "FLZ025"
NWS_API_URL = "https://api.weather.gov"

VPN_PEER_IP = "10.0.0.2"
ALERT_EMAIL = "lbornacelli@gmail.com"
EC2_INSTANCE_ID = "i-00adbd5534f0684b0"

BASE_DIR = os.path.expanduser("~/addylabs")
OUTPUTS_DIR = f"{BASE_DIR}/outputs"
LOGS_DIR = f"{BASE_DIR}/logs"

# Private subnet for RDS/ElastiCache
PRIVATE_SUBNET_ID = 'subnet-02cb183077dd3f022'
RDS_SG_ID = 'sg-0acb2c1806767634c'
NEW_VPC_ID = 'vpc-025e14e1244cbc365'

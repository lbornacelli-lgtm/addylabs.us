# AddyLabs AI Platform

A reusable hybrid cloud AI platform built on AWS EC2 + On-Prem Ubuntu.

## Architecture
- **On-Prem:** Dell OptiPlex 7090 · Ubuntu 24.04 · 192.168.22.115
- **AWS EC2:** t3.micro · Ubuntu 22.04 · 13.216.168.199
- **VPN:** WireGuard tunnel · 10.0.0.1 ↔ 10.0.0.2

## Services
| Service | Port | URL |
|---------|------|-----|
| LiteLLM Proxy | 4000 | http://13.216.168.199:4000 |
| RStudio Server | 8787 | https://rstudio.addylabs.us |
| Piper TTS | 5050 | http://localhost:5050 |
| Kokoro TTS | 5051 | http://localhost:5051 |

## AI Models
- claude-sonnet (Anthropic)
- bedrock-llama (AWS Bedrock)
- piper-tts (Local)
- kokoro-tts (Local)
- elevenlabs-tts (Cloud)

## Agents
- **content_agent.py** — AI content generation
- **tts_agent.py** — TTS routing (Piper/Kokoro/ElevenLabs)
- **weather_agent.py** — NWS/NOAA weather broadcast scripts
- **monitor_agent.py** — Infrastructure health monitoring

## Usage
```bash
cd ~/addylabs

# Generate content
python3 agents/content_agent.py "Topic here"

# Text to speech
python3 agents/tts_agent.py kokoro "Hello world"
python3 agents/tts_agent.py elevenlabs "Hello world"

# Weather broadcast
python3 agents/weather_agent.py

# Infrastructure monitor
python3 agents/monitor_agent.py
```

## Storage
- S3 Media: lawborn-media-files
- S3 ETL: lawborn-etl-data
- S3 Static: lawborn-static-assets
- SQS ETL: lawborn-etl-jobs
- SQS Background: lawborn-background-jobs

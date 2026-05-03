import requests
import sys
sys.path.append('/home/ubuntu/addylabs')
from config.settings import LITELLM_BASE_URL, DEFAULT_AI_MODEL, DEFAULT_TTS_MODEL

def chat(prompt, model=None, system=None):
    model = model or DEFAULT_AI_MODEL
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    response = requests.post(
        f"{LITELLM_BASE_URL}/v1/chat/completions",
        json={"model": model, "messages": messages},
        timeout=60
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def tts(text, model=None, output_file=None):
    model = model or DEFAULT_TTS_MODEL
    response = requests.post(
        f"{LITELLM_BASE_URL}/v1/audio/speech",
        json={"model": model, "input": text, "voice": "alloy"},
        timeout=60
    )
    response.raise_for_status()
    if output_file:
        with open(output_file, "wb") as f:
            f.write(response.content)
    return response.content

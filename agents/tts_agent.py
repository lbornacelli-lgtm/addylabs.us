import sys
sys.path.append('/home/ubuntu/addylabs')
from config.settings import OUTPUTS_DIR, ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID
import datetime
import subprocess

def speak(text, engine="kokoro", output_file=None):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_file or f"{OUTPUTS_DIR}/audio_{timestamp}.wav"

    if engine == "piper":
        subprocess.run([
            "python3", "-m", "piper",
            "--model", "/home/ubuntu/tts/piper/en_US-lessac-medium.onnx",
            "--output_file", output_file
        ], input=text.encode(), check=True)

    elif engine == "kokoro":
        from kokoro_onnx import Kokoro
        import soundfile as sf
        kokoro = Kokoro(
            "/home/ubuntu/tts/kokoro/kokoro-v1.0.onnx",
            "/home/ubuntu/tts/kokoro/voices-v1.0.bin"
        )
        samples, sample_rate = kokoro.create(text, voice="af_heart", speed=1.0, lang="en-us")
        sf.write(output_file, samples, sample_rate)

    elif engine == "elevenlabs":
        from elevenlabs.client import ElevenLabs
        from elevenlabs import save
        client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        audio = client.text_to_speech.convert(
            text=text,
            voice_id=ELEVENLABS_VOICE_ID,
            model_id="eleven_multilingual_v2"
        )
        output_file = output_file.replace(".wav", ".mp3")
        save(audio, output_file)

    print(f"Audio saved to {output_file}")
    return output_file

if __name__ == "__main__":
    engine = sys.argv[1] if len(sys.argv) > 1 else "kokoro"
    text = sys.argv[2] if len(sys.argv) > 2 else "AddyLabs TTS agent is online!"
    speak(text, engine=engine)

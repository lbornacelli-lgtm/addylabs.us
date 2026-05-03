import sys
sys.path.append('/home/ubuntu/addylabs')
import requests
from utils.litellm_client import chat
from config.prompts import WEATHER_AGENT_PROMPT
from config.settings import NWS_API_URL, NWS_ZONE, OUTPUTS_DIR
import datetime

def get_weather():
    # Use coordinates for Gainesville FL instead of zone code
    url = "https://api.weather.gov/points/29.6742,-82.3363"
    headers = {"User-Agent": "AddyLabs/1.0 lbornacelli@gmail.com"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    forecast_url = response.json()["properties"]["forecast"]
    forecast = requests.get(forecast_url, headers=headers, timeout=10)
    forecast.raise_for_status()
    periods = forecast.json()["properties"]["periods"][:3]
    raw = "\n".join([f"{p['name']}: {p['detailedForecast']}" for p in periods])
    return raw

def generate_weather_broadcast():
    print("Fetching NWS weather data for Gainesville FL...")
    raw_weather = get_weather()
    print("Generating broadcast script...")
    script = chat(raw_weather, system=WEATHER_AGENT_PROMPT)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    outfile = f"{OUTPUTS_DIR}/weather_{timestamp}.txt"
    with open(outfile, "w") as f:
        f.write(script)
    print(f"Weather broadcast saved to {outfile}")
    return script

if __name__ == "__main__":
    print(generate_weather_broadcast())

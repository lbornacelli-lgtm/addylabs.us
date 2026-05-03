import sys
sys.path.append('/home/ubuntu/addylabs')
from utils.litellm_client import chat
from config.prompts import CONTENT_AGENT_PROMPT
from config.settings import OUTPUTS_DIR
import datetime
import os

def generate_content(topic, content_type="broadcast", model=None):
    print(f"Generating {content_type} content for: {topic}")
    prompt = f"Create a {content_type} script about: {topic}"
    content = chat(prompt, model=model, system=CONTENT_AGENT_PROMPT)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    outfile = f"{OUTPUTS_DIR}/content_{timestamp}.txt"
    with open(outfile, "w") as f:
        f.write(content)
    print(f"Content saved to {outfile}")
    return content

if __name__ == "__main__":
    topic = sys.argv[1] if len(sys.argv) > 1 else "Today's top stories"
    print(generate_content(topic))

import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Create data folder if it doesn't exist
os.makedirs("data", exist_ok=True)

SYSTEM_PROMPT = """
You are a viral YouTube Shorts script generator.
You create short, creepy, curiosity-driven space facts.
Facts must be accurate and under 10 words.
"""

USER_PROMPT = """
Generate 3 creepy space facts.
Tone: dark, mysterious.
Return JSON only in this format:

{
  "topic": "Creepy Space Facts",
  "facts": ["fact 1", "fact 2", "fact 3"]
}
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_PROMPT}
    ],
    temperature=0.8
)

data = json.loads(response.choices[0].message.content)

# Unique filename with timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"data/facts_{timestamp}.json"

with open(filename, "w") as f:
    json.dump(data, f, indent=2)

print(f"✅ Facts saved to: {filename}")
print(json.dumps(data, indent=2))
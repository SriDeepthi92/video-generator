import os
import json
import base64
from io import BytesIO
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DATA_DIR = "data"
IMAGE_DIR = "images"

# Ensure image directory exists
os.makedirs(IMAGE_DIR, exist_ok=True)

def get_latest_facts_file():
    files = [
        os.path.join(DATA_DIR, f)
        for f in os.listdir(DATA_DIR)
        if f.startswith("facts_") and f.endswith(".json")
    ]
    if not files:
        raise FileNotFoundError("No facts files found in data/")
    return max(files, key=os.path.getmtime)

# 1️⃣ Load latest facts
facts_file = get_latest_facts_file()

with open(facts_file, "r") as f:
    facts_data = json.load(f)

topic = facts_data["topic"]
facts = facts_data["facts"]

# 2️⃣ Build image prompt dynamically
facts_text = ", ".join(facts)

prompt = f"""
Cinematic, dark illustration related to: {topic}.
Visualize the mood of these ideas: {facts_text}.
Deep space setting, eerie atmosphere,
high detail, dramatic lighting,
vertical composition, realistic.
"""

# 3️⃣ Generate image
result = client.images.generate(
    model="gpt-image-1",
    prompt=prompt,
    size="1024x1536"
)

image_base64 = result.data[0].b64_json
image_bytes = base64.b64decode(image_base64)
image = Image.open(BytesIO(image_bytes))

# 4️⃣ Save image with matching timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
image_filename = f"{IMAGE_DIR}/image_{timestamp}.png"
image.save(image_filename)

print("🧠 Used facts file:", facts_file)
print("🖼️ Image saved to:", image_filename)
print("📝 Topic:", topic)
print("📝 Facts:", facts)

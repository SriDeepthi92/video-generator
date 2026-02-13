import os
import json
from moviepy import (
    ImageClip,
    TextClip,
    CompositeVideoClip,
    concatenate_videoclips
)

DATA_FILE = "data/olympics_facts.json"
IMAGE_DIR = "images/olympics"
VIDEO_DIR = "videos"
os.makedirs(VIDEO_DIR, exist_ok=True)

VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
DURATION_PER_FACT = 4
FONT_PATH = "C:/Windows/Fonts/arial.ttf"

# Load facts
with open(DATA_FILE, "r") as f:
    facts = json.load(f)["facts"]

# Load images
images = sorted(
    [
        os.path.join(IMAGE_DIR, f)
        for f in os.listdir(IMAGE_DIR)
        if f.endswith(".jpg")
    ]
)

assert len(images) >= len(facts), "Not enough images for facts"

clips = []

for fact, img_path in zip(facts, images):
    # Background with Ken Burns
    bg = (
        ImageClip(img_path)
        .resized(height=VIDEO_HEIGHT)
        .with_duration(DURATION_PER_FACT)
        .resized(lambda t: 1 + 0.08 * (t / DURATION_PER_FACT))
    )

    # Text overlay
    txt = (
        TextClip(
            text=fact,
            method="caption",
            size=(900, 400),
            font=FONT_PATH,
            font_size=80,
            color="white",
            text_align="center"
        )
        .with_position(("center", "center"))
        .with_duration(DURATION_PER_FACT)
    )

    # Combine image + text for THIS segment
    segment = CompositeVideoClip(
        [bg, txt],
        size=(VIDEO_WIDTH, VIDEO_HEIGHT)
    )

    clips.append(segment)

# ✅ THIS IS THE IMPORTANT PART
final_video = concatenate_videoclips(clips, method="compose")

output_path = os.path.join(VIDEO_DIR, "olympics_short.mp4")
final_video.write_videofile(
    output_path,
    fps=30,
    codec="libx264",
    audio=False
)

print("🏅 Olympics video generated:", output_path)

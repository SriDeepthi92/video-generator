import os
import json
from datetime import datetime
from moviepy import ImageClip, TextClip, CompositeVideoClip, vfx

DATA_DIR = "data"
IMAGE_DIR = "images"
VIDEO_DIR = "videos"

os.makedirs(VIDEO_DIR, exist_ok=True)

VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
DURATION_PER_FACT = 4

def get_latest_file(folder, prefix, suffix):
    files = [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.startswith(prefix) and f.endswith(suffix)
    ]
    if not files:
        raise FileNotFoundError(f"No {prefix} files found in {folder}")
    return max(files, key=os.path.getmtime)

# 🔹 Load existing files only (NO API CALLS)
facts_file = get_latest_file(DATA_DIR, "facts_", ".json")
image_file = get_latest_file(IMAGE_DIR, "space_", ".png")

with open(facts_file, "r") as f:
    facts_data = json.load(f)

facts = facts_data["facts"]

total_duration = len(facts) * DURATION_PER_FACT

# Background image with Ken Burns effect (slow zoom + pan)
ken_burns_zoom = 0.12
ken_burns_pan_x = 50
ken_burns_pan_y = 40

bg = (
    ImageClip(image_file)
    .resized(height=VIDEO_HEIGHT)
    .with_duration(total_duration)
    .resized(lambda t: 1 + ken_burns_zoom * (t / total_duration))
    .with_position(
        lambda t: (
            int(-ken_burns_pan_x * (t / total_duration)),
            int(-ken_burns_pan_y * (t / total_duration)),
        )
    )
)



clips = [bg]

FONT_PATH = "C:/Windows/Fonts/arial.ttf"
TEXT_BOX_WIDTH = 900
TEXT_BOX_HEIGHT = 400  # REQUIRED for caption mode


for i, fact in enumerate(facts):
    txt = (
        TextClip(
            text=fact,
            method="caption",
            size=(TEXT_BOX_WIDTH, TEXT_BOX_HEIGHT),
            font=FONT_PATH,
            font_size=80,
            color="white",
            text_align="center",
        )
        .with_position(("center", "center"))
        .with_start(i * DURATION_PER_FACT)
        .with_duration(DURATION_PER_FACT)
        .with_effects([vfx.FadeIn(0.5), vfx.FadeOut(0.5)])
    )
    clips.append(txt)


final_video = CompositeVideoClip(clips, size=(VIDEO_WIDTH, VIDEO_HEIGHT)).with_duration(total_duration)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_path = f"{VIDEO_DIR}/short_TEST_{timestamp}.mp4"

final_video.write_videofile(
    output_path,
    fps=30,
    codec="libx264",
    audio=False
)

print("🎬 Test video generated:", output_path)

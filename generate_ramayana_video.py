import os
import re
from moviepy import ImageClip, concatenate_videoclips


def _serial_from_filename(filename: str) -> int:
    name_without_ext = os.path.splitext(filename)[0]
    match = re.search(r"\d+", name_without_ext)
    if not match:
        raise ValueError(f"No serial number found in filename: {filename}")
    return int(match.group())


def generate_video_from_serial_images(
    image_folder: str,
    output_path: str,
    image_duration: float = 2.0,
    fps: int = 30,
) -> str:
    allowed_extensions = {".jpg", ".jpeg", ".png", ".webp"}

    image_files = [
        file_name
        for file_name in os.listdir(image_folder)
        if os.path.isfile(os.path.join(image_folder, file_name))
        and os.path.splitext(file_name.lower())[1] in allowed_extensions
    ]

    if not image_files:
        raise FileNotFoundError(f"No images found in folder: {image_folder}")

    ordered_images = sorted(image_files, key=_serial_from_filename)

    clips = [
        ImageClip(os.path.join(image_folder, file_name)).with_duration(image_duration)
        for file_name in ordered_images
    ]

    final_video = concatenate_videoclips(clips, method="compose")

    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    final_video.write_videofile(
        output_path,
        fps=fps,
        codec="libx264",
        audio=False,
    )

    final_video.close()
    for clip in clips:
        clip.close()

    return output_path


if __name__ == "__main__":
    source_folder = r"C:\Users\sride\Downloads\Ramayana"
    output_file = os.path.join("videos", "ramayana_ordered.mp4")

    video_path = generate_video_from_serial_images(
        image_folder=source_folder,
        output_path=output_file,
        image_duration=2.5,
        fps=30,
    )

    print(f"🎬 Video generated successfully: {video_path}")

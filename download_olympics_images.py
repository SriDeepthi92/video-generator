import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

UNSPLASH_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
BASE_IMAGE_DIR = "images/olympics"
os.makedirs(BASE_IMAGE_DIR, exist_ok=True)

def download_images(query, count=3):
    url = "https://api.unsplash.com/search/photos"
    headers = {"Authorization": f"Client-ID {UNSPLASH_KEY}"}
    params = {
        "query": query,
        "orientation": "portrait",
        "per_page": count
    }

    r = requests.get(url, headers=headers, params=params)
    r.raise_for_status()
    results = r.json()["results"]

    paths = []

    for i, photo in enumerate(results[:count]):
        image_url = photo["urls"]["regular"]
        photographer = photo["user"]["name"]
        photo_url = photo["links"]["html"]

        img_bytes = requests.get(image_url).content
        filename = f"olympics_{i+1}.jpg"
        path = os.path.join(BASE_IMAGE_DIR, filename)

        with open(path, "wb") as f:
            f.write(img_bytes)

        attribution = {
            "source": "Unsplash",
            "photographer": photographer,
            "photo_url": photo_url,
            "credit": f"Photo by {photographer} on Unsplash"
        }

        with open(path.replace(".jpg", ".json"), "w") as f:
            json.dump(attribution, f, indent=2)

        paths.append(path)
        print("🖼️ Downloaded:", path)

    return paths


if __name__ == "__main__":
    download_images("olympics athletes stadium competition", 3)

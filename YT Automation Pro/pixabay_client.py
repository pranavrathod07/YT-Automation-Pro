import random
import requests
import os
from config import PIXABAY_API_KEY, SPORT_QUERIES, TEMP_DIR


def fetch_unused_sports_video(used_ids, max_attempts=8):
    """
    Random sports query se Pixabay par video search karta hai,
    aur ek aisa video return karta hai jo pehle use nahi hua.
    Returns: dict {id, download_url} ya None
    """
    random.shuffle(SPORT_QUERIES)

    for query in SPORT_QUERIES[:max_attempts]:
        resp = requests.get(
            "https://pixabay.com/api/videos/",
            params={
                "key": PIXABAY_API_KEY,
                "q": query,
                "per_page": 20,
                "safesearch": "true",
                "video_type": "film",  # sirf real human/live footage, animation/cartoon exclude
            },
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        hits = data.get("hits", [])
        random.shuffle(hits)

        for hit in hits:
            vid = hit["id"]
            if vid in used_ids:
                continue
            # medium quality usually best balance of size/resolution
            video_files = hit["videos"]
            url = (
                video_files.get("medium", {}).get("url")
                or video_files.get("large", {}).get("url")
                or video_files.get("small", {}).get("url")
            )
            if url:
                return {"id": vid, "url": url, "query": query}

    return None  # kuch nahi mila, saare exhaust ho gaye is batch me


def download_video(url, dest_path=None):
    os.makedirs(TEMP_DIR, exist_ok=True)
    dest_path = dest_path or os.path.join(TEMP_DIR, "source_clip.mp4")
    r = requests.get(url, stream=True, timeout=60)
    r.raise_for_status()
    with open(dest_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    return dest_path

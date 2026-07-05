import json
import requests
from config import GEMINI_API_KEY, GEMINI_MODEL


def generate_metadata(sport_query, song_name):
    """
    Gemini se ek catchy YouTube Shorts title, description aur tags generate karwata hai.
    Returns dict: {title, description, tags: [list]}
    """
    prompt = f"""
You are a viral YouTube Shorts copywriter.
The short video shows: {sport_query} highlights/action clip.
Background music is a phonk song called: {song_name}.

Return ONLY valid JSON, no markdown, no backticks, in this exact format:
{{
  "title": "short punchy title under 70 characters, include emoji if it fits",
  "description": "2-3 line engaging description, include a call to action to subscribe, and 3-4 relevant hashtags at the end",
  "tags": ["tag1", "tag2", "tag3", "... up to 15 short tags relevant to sports shorts and phonk edits"]
}}
"""

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    )
    body = {"contents": [{"parts": [{"text": prompt}]}]}

    resp = requests.post(url, json=body, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    text = data["candidates"][0]["content"]["parts"][0]["text"]
    text = text.strip().strip("```").replace("json\n", "").strip()

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        # fallback agar Gemini ne thoda alag format diya
        parsed = {
            "title": f"{sport_query.title()} Edit 🔥",
            "description": f"Sports edit with {song_name}. Subscribe for daily shorts! #shorts #sports #phonk",
            "tags": ["shorts", "sports", "phonk", "edit", "viral"],
        }

    return parsed

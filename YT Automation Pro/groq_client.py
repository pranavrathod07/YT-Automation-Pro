"""
Groq (free, fast) - Gemini ka alternative.
API key yaha se lo (free): https://console.groq.com/keys
.env me daalo: GROQ_API_KEY=your_key
"""
import json
import requests
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")


def generate_metadata(sport_query, song_name):
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

    resp = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
        json={
            "model": GROQ_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.8,
        },
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    text = data["choices"][0]["message"]["content"].strip()
    text = text.strip("`").replace("json\n", "").strip()

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        parsed = {
            "title": f"{sport_query.title()} Edit 🔥",
            "description": f"Sports edit with {song_name}. Subscribe for daily shorts! #shorts #sports #phonk",
            "tags": ["shorts", "sports", "phonk", "edit", "viral"],
        }

    return parsed

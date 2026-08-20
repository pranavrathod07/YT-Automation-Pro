"""
Groq (free, fast) - Gemini ka alternative.
API key yaha se lo (free): https://console.groq.com/keys
.env me daalo: GROQ_API_KEY=your_key
"""
import json
import requests
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
# Strictly forced model name
GROQ_MODEL = os.getenv("GROQ_MODEL") or "llama-3.1-8b-instant"


def generate_metadata(sport_query, song_name):
    # Fallback JSON structure agar API bilkul fail ho jaye
    default_metadata = {
        "title": f"{sport_query.title()} Highlights Edit 🔥",
        "description": f"Amazing {sport_query} sports edit synced with {song_name}. Subscribe for more daily shorts!\n\n#shorts #sports #{sport_query.replace(' ', '')} #phonk",
        "tags": ["shorts", "sports", sport_query, "phonk", "edit", "viral", "trending"]
    }

    if not GROQ_API_KEY:
        print("WARNING: GROQ_API_KEY missing! Using default metadata.")
        return default_metadata

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

    try:
        resp = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": GROQ_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.8,
            },
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()
        text = data["choices"][0]["message"]["content"].strip()
        text = text.strip("`").replace("json\n", "").strip()
        parsed = json.loads(text)
        return parsed

    except Exception as e:
        print(f"WARNING: Groq API Error ({e}). Switching to default fallback metadata.")
        return default_metadata

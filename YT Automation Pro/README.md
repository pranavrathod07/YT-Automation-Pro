# 🎬 YT Shorts Automation

Fully automated pipeline that generates and uploads YouTube Shorts on a schedule — combining free stock sports footage with your own music, AI-generated titles/descriptions/tags, and direct upload to one or more YouTube channels.

## ✨ Features

- 🎥 Pulls royalty-free sports/action stock footage automatically from **Pixabay**
- 🎵 Cycles through your own local music library (no repeats until the full library has played)
- ✂️ Auto-edits footage into a vertical 9:16 Short with `ffmpeg`
- 🤖 Generates catchy titles, descriptions, and tags with AI (**Groq**, free tier)
- ⬆️ Uploads directly to YouTube via the official YouTube Data API v3
- 👥 **Multi-account support** — run the exact same pipeline across multiple YouTube channels, each with independent history/state
- ⏰ Designed to run on a schedule (cron / Windows Task Scheduler) — fully hands-off
- 🔁 Tracks used clips and song rotation so content never repeats until the pool is exhausted

## 🏗️ How it works

```
Pixabay (stock clip) ─┐
                       ├─► ffmpeg (combine + crop to 9:16) ─► Groq AI (title/desc/tags) ─► YouTube Data API (upload)
Local song library ────┘
```

State (which song is next, which clips were already used) is tracked per-account in `data/`, so multiple channels never collide with each other.

## 📋 Prerequisites

- Python 3.10+
- [ffmpeg](https://ffmpeg.org/download.html) installed and available on PATH
- A [Pixabay API key](https://pixabay.com/api/docs/) (free)
- A [Groq API key](https://console.groq.com/keys) (free)
- A Google Cloud project with the **YouTube Data API v3** enabled + an OAuth 2.0 Desktop client

## 🚀 Setup

### 1. Clone and install

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment variables

```bash
cp .env.example .env
```

Fill in your `PIXABAY_API_KEY` and `GROQ_API_KEY` in `.env`.

### 3. Set up YouTube OAuth (one-time, per Google Cloud project)

1. Go to [Google Cloud Console](https://console.cloud.google.com/) → create/select a project
2. Enable **YouTube Data API v3** (APIs & Services → Library)
3. Go to APIs & Services → Credentials → **Create Credentials → OAuth client ID**
   → Application type: **Desktop app**
4. Download the JSON, rename it to `client_secret.json`, and place it in the project root

### 4. Add your music

Drop your `.mp3` / `.wav` / `.m4a` files into the `songs/` folder. They will be cycled through in order.

### 5. Configure accounts

Edit `config.py`:

```python
ACCOUNTS = [
    "channel1",
    "channel2",
]
```

Each name is just a label used to keep each channel's login token and history separate — use anything you like.

### 6. Authorize each YouTube channel (one-time per channel)

```bash
python youtube_uploader.py --authorize channel1
```

A browser window opens — log in with the Google account for that channel and grant access. Repeat for every account in `ACCOUNTS`.

> ⚠️ If your OAuth consent screen is in **Testing** mode, add every Google account you'll use as a **Test user** in the consent screen settings, or the login will be blocked.

### 7. Run it

```bash
python main.py
```

This generates and uploads one Short per configured account.

## ⏰ Scheduling

### Windows

Run the included helper script to auto-create two daily scheduled tasks:

```powershell
powershell -ExecutionPolicy Bypass -File setup_scheduler.ps1
```

This creates tasks that run daily at 12:00 AM and 7:00 PM.

### Linux / macOS (cron)

```bash
crontab -e
```

```
0 0 * * *  cd /path/to/project && /path/to/venv/bin/python main.py >> logs/cron.log 2>&1
0 19 * * * cd /path/to/project && /path/to/venv/bin/python main.py >> logs/cron.log 2>&1
```

## 📁 Project structure

```
.
├── main.py               # Orchestrates the full pipeline for all accounts
├── config.py              # All configuration (accounts, paths, search terms)
├── state_manager.py        # Tracks song rotation + used clips per account
├── pixabay_client.py       # Fetches stock footage from Pixabay
├── video_builder.py        # ffmpeg-based video/audio combination
├── groq_client.py          # AI-generated metadata via Groq
├── youtube_uploader.py     # OAuth + YouTube Data API upload logic
├── setup_scheduler.ps1     # Windows Task Scheduler automation
├── songs/                  # Your local music library (not committed)
└── data/, logs/, tokens/   # Runtime state (not committed)
```

## ⚠️ Important notes

- **Copyright**: Only use music/audio you own or that is properly licensed for redistribution. Uploading copyrighted tracks without rights can result in Content ID claims or channel strikes.
- **Stock footage only**: This project intentionally uses generic royalty-free stock footage (via Pixabay), not real athlete/broadcast footage, to avoid copyright issues.
- **API quotas**: The YouTube Data API free quota is 10,000 units/day; each upload costs ~1,600 units, so a handful of daily uploads per account comfortably fits within the free tier.
- Never commit `.env`, `client_secret.json`, or anything in `tokens/` — these are already excluded via `.gitignore`.

## 🛠️ Tech stack

Python · ffmpeg · Pixabay API · Groq API · YouTube Data API v3

## 📄 License

MIT — see [LICENSE](LICENSE).

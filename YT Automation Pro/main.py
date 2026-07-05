import os
import glob
import logging
import traceback
from datetime import datetime

from config import SONGS_DIR, PRIVACY_STATUS, LOGS_DIR, TEMP_DIR, ACCOUNTS
from state_manager import load_state, save_state, get_next_song, mark_video_used
from pixabay_client import fetch_unused_sports_video, download_video
from video_builder import build_short
from groq_client import generate_metadata  # Gemini quota issue ki wajah se Groq use kar rahe hai
# from gemini_client import generate_metadata  # agar Gemini wapas use karna ho to ye uncomment karo
from youtube_uploader import upload_short

os.makedirs(LOGS_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOGS_DIR, "automation.log"),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


def get_songs_list():
    exts = ("*.mp3", "*.wav", "*.m4a")
    files = []
    for ext in exts:
        files.extend(glob.glob(os.path.join(SONGS_DIR, ext)))
    return sorted(files)


def run_once_for_account(account):
    """Ek single YouTube account ke liye ek short banake upload karta hai.
    Har account ki apni alag state (song cycle + used clips) hoti hai,
    isliye accounts ek dusre se independent chalte hai."""
    log = logging.getLogger()
    log.info(f"=== [{account}] Automation run started ===")

    state = load_state(account)

    songs = get_songs_list()
    if not songs:
        raise RuntimeError(f"'{SONGS_DIR}' folder me koi song nahi mila (.mp3/.wav/.m4a).")

    song_path = get_next_song(state, songs)
    song_name = os.path.splitext(os.path.basename(song_path))[0]
    log.info(f"[{account}] Selected song: {song_name}")

    video_info = fetch_unused_sports_video(state["used_pixabay_ids"])
    if not video_info:
        log.info(f"[{account}] All pixabay clips used once, resetting history.")
        state["used_pixabay_ids"] = []
        video_info = fetch_unused_sports_video(state["used_pixabay_ids"])
        if not video_info:
            raise RuntimeError("Pixabay se koi video nahi mil paaya.")

    log.info(f"[{account}] Fetched pixabay video id={video_info['id']} query='{video_info['query']}'")
    raw_clip = download_video(video_info["url"], dest_path=os.path.join(TEMP_DIR, f"source_{account}.mp4"))

    final_video = build_short(raw_clip, song_path, output_path=os.path.join(TEMP_DIR, f"final_{account}.mp4"))
    log.info(f"[{account}] Final short built at {final_video}")

    meta = generate_metadata(video_info["query"], song_name)
    log.info(f"[{account}] Generated title: {meta['title']}")

    video_id = upload_short(
        account,
        final_video,
        title=meta["title"],
        description=meta["description"],
        tags=meta["tags"],
        privacy_status=PRIVACY_STATUS,
    )

    mark_video_used(state, video_info["id"])
    save_state(account, state)

    for f in (raw_clip, final_video):
        try:
            os.remove(f)
        except OSError:
            pass

    log.info(f"=== [{account}] Run finished successfully. YouTube video id: {video_id} ===")
    print(f"[{account}] Done! Uploaded video id: {video_id}")


def run_once():
    """Config me jitne bhi accounts likhe hai, sabke liye ek-ek short banake upload karta hai."""
    if not ACCOUNTS:
        raise RuntimeError("config.py me ACCOUNTS list khali hai, kam se kam ek account add karo.")

    errors = []
    for account in ACCOUNTS:
        try:
            run_once_for_account(account)
        except Exception as e:
            logging.getLogger().error(f"[{account}] Run failed: {e}\n{traceback.format_exc()}")
            print(f"[{account}] ERROR: {e}")
            errors.append((account, e))

    if errors:
        raise RuntimeError(f"{len(errors)} account(s) failed: {[a for a, _ in errors]}")


if __name__ == "__main__":
    run_once()

import subprocess
import os
from config import SHORT_DURATION, VIDEO_WIDTH, VIDEO_HEIGHT, TEMP_DIR


def build_short(video_path, audio_path, output_path=None):
    """
    - video_path ko loop karta hai (agar chota ho) taaki duration pura ho
    - vertical 9:16 (1080x1920) me crop/scale karta hai
    - audio ko song se replace karta hai
    - final duration = SHORT_DURATION seconds
    """
    os.makedirs(TEMP_DIR, exist_ok=True)
    output_path = output_path or os.path.join(TEMP_DIR, "final_short.mp4")

    vf = (
        f"scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}:force_original_aspect_ratio=increase,"
        f"crop={VIDEO_WIDTH}:{VIDEO_HEIGHT},setsar=1"
    )

    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1", "-i", video_path,   # video ko loop karo agar chota hai
        "-i", audio_path,                          # phonk song
        "-t", str(SHORT_DURATION),
        "-vf", vf,
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        output_path,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg failed:\n{result.stderr}")

    return output_path

#!/usr/bin/env python3
"""
Full Autonomous Pipeline:
1. Clip 50s from high-res No-Facecam Gameplay Stream
2. Generate natural Hinglish story-mode script
3. Voice dub in Prashast's cloned voice via Cartesia Sonic
4. Crop & Re-frame to 9:16 Vertical Short (1080x1920)
5. Upload to YouTube Channel Gaming World
"""

import os
import sys
import subprocess
from cartesia_tts import synthesize_prashast_voice
from youtube_helper import upload_short

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Curated "No Facecam / No Commentary" High Quality Gameplay Channels
NO_FACECAM_STREAM_SOURCES = [
    "https://www.youtube.com/watch?v=QdBZY2fkU-0", # GTA 6 Trailer 4K official
]

SAMPLE_HINGLISH_SCRIPT = (
    "Bhai, ye GTA 6 ka mission literally impossible lag raha hai! "
    "Jason stealthily bank vault me enter karta hai, par jaise hi alarm trigger hota hai, "
    "poori Vice City police alert ho jati hai! "
    "Aur tab Lucia full aggressive mode me aati hai with heavy firepower! "
    "Aapko kya lagta hai, kya ye escape successful hoga? "
    "Comment me batao aur daily GTA 6 gameplay ke liye Gaming World ko abhi subscribe karo!"
)

def download_and_crop_segment(video_url, start_time="00:00:10", duration="00:00:52", output_path="clip_vertical.mp4"):
    print(f"Downloading {duration} segment from stream...")
    raw_clip = os.path.join(SCRIPT_DIR, "raw_clip.mp4")
    
    # Download exact segment using yt-dlp
    download_cmd = [
        "yt-dlp",
        "--download-sections", f"*{start_time}-{start_time}+52",
        "-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
        "--merge-output-format", "mp4",
        "-o", raw_clip,
        video_url,
        "--force-overwrites"
    ]
    subprocess.run(download_cmd, check=True)
    return raw_clip

def render_vertical_short_with_voice(raw_video, voice_audio, output_short):
    print("Cropping 16:9 to vertical 9:16 (1080x1920) & mixing Prashast's voice...")
    # Crop to 9:16 center, lower background in-game audio volume to 15%, overlay Prashast cloned voice at 100%
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-i", raw_video,
        "-i", voice_audio,
        "-filter_complex",
        "[0:v]crop=ih*(9/16):ih,scale=1080:1920[v];"
        "[0:a]volume=0.15[game_audio];"
        "[game_audio][1:a]amix=inputs=2:duration=first[a]",
        "-map", "[v]",
        "-map", "[a]",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "22",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_short
    ]
    subprocess.run(ffmpeg_cmd, check=True)
    print(f"Ready: {output_short}")

if __name__ == "__main__":
    print("Pipeline ready for autonomous execution.")

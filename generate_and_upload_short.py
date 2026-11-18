#!/usr/bin/env python3
"""
Generate a transformative Hindi-dubbed GTA 6 News Short with Prashast's Cloned Voice & Upload to YouTube
"""

import os
import sys
import asyncio
import subprocess
from PIL import Image, ImageDraw
import edge_tts
from cartesia_tts import synthesize_prashast_voice

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_AUDIO = os.path.join(SCRIPT_DIR, "hindi_voiceover.wav")
OUTPUT_IMAGE = os.path.join(SCRIPT_DIR, "short_slide.png")
OUTPUT_VIDEO = os.path.join(SCRIPT_DIR, "gta6_news_short.mp4")

HINDI_SCRIPT = (
    "Doston, GTA 6 ko lekar bohot bada update aaya hai! "
    "Rockstar Games ne confirm kiya hai ki Vice City aur Leonida ka map GTA 5 se double bada hone wala hai! "
    "Crazy graphics aur naye missions ke liye Gaming World ko abhi subscribe karein!"
)

def generate_voice(text, output_file):
    print("Generating audio using cloned voice 'Prashast' via Cartesia Sonic...")
    success = synthesize_prashast_voice(text, output_file, language="hi")
    if not success:
        print("Falling back to Edge TTS...")
        asyncio.run(edge_tts.Communicate(text, voice="hi-IN-MadhurNeural").save(output_file))

def create_vertical_short_image(output_image):
    print("Creating vertical 9:16 Short graphic (1080x1920)...")
    width, height = 1080, 1920
    img = Image.new("RGB", (width, height), color=(15, 10, 25))
    draw = ImageDraw.Draw(img)

    for y in range(450):
        r = int(245 * (1 - y/450) + 15 * (y/450))
        g = int(35 * (1 - y/450) + 10 * (y/450))
        b = int(110 * (1 - y/450) + 25 * (y/450))
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    draw.rectangle([(60, 140), (1020, 320)], fill=(255, 215, 0))
    draw.text((100, 200), "🔥 GTA 6 BIG NEWS UPDATE!", fill=(0, 0, 0))

    draw.rectangle([(50, 440), (1030, 1420)], fill=(30, 18, 50), outline=(0, 255, 204), width=8)
    draw.text((100, 520), "LEONIDA MAP DETAILS", fill=(255, 45, 120))
    draw.text((100, 680), "• 2X Bigger than GTA 5 Map", fill=(255, 255, 255))
    draw.text((100, 820), "• Vice City Neon Beaches & Swamps", fill=(255, 255, 255))
    draw.text((100, 960), "• Unpredictable NPC AI System", fill=(255, 255, 255))
    draw.text((100, 1100), "• Dual Protagonists: Jason & Lucia", fill=(255, 255, 255))
    draw.text((100, 1240), "• Coming 2026 to Next-Gen Consoles", fill=(255, 215, 0))

    draw.rectangle([(60, 1500), (1020, 1680)], fill=(255, 45, 120))
    draw.text((140, 1560), "SUBSCRIBE: @GAMINGWORLDSWAGGERS", fill=(255, 255, 255))

    img.save(output_image)
    print(f"Image saved to: {output_image}")

def build_short_video(image_path, audio_path, video_path):
    print("Assembling Short video with ffmpeg...")
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", image_path,
        "-i", audio_path,
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-shortest",
        video_path
    ]
    subprocess.run(cmd, check=True)
    print(f"Short video successfully created: {video_path}")

def main():
    generate_voice(HINDI_SCRIPT, OUTPUT_AUDIO)
    create_vertical_short_image(OUTPUT_IMAGE)
    build_short_video(OUTPUT_IMAGE, OUTPUT_AUDIO, OUTPUT_VIDEO)
    print("READY_FOR_UPLOAD")

if __name__ == "__main__":
    main()

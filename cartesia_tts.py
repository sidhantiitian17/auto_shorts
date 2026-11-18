#!/usr/bin/env python3
"""
Cartesia TTS Integration for Prashast Cloned Voice
"""

import os
import requests

CARTESIA_API_KEY = "sk_car_mnfYL5oVbaxCmAyC5dkHGS"
PRASHAST_VOICE_ID = "1742dc37-bd3c-4321-80a0-fd5bbd5a0ae5"

def synthesize_prashast_voice(text: str, output_file: str, language: str = "hi") -> bool:
    url = "https://api.cartesia.ai/tts/bytes"
    headers = {
        "X-API-Key": CARTESIA_API_KEY,
        "Cartesia-Version": "2024-06-10",
        "Content-Type": "application/json"
    }
    payload = {
        "model_id": "sonic-latest",
        "transcript": text,
        "voice": {
            "mode": "id",
            "id": PRASHAST_VOICE_ID
        },
        "output_format": {
            "container": "wav",
            "encoding": "pcm_s16le",
            "sample_rate": 44100
        },
        "language": language
    }

    import time
    for attempt in range(1, 5):
        try:
            print(f"Synthesizing with Cartesia using cloned voice 'Prashast' (Attempt {attempt})...")
            resp = requests.post(url, headers=headers, json=payload, timeout=120)
            if resp.status_code == 200:
                with open(output_file, "wb") as f:
                    f.write(resp.content)
                print(f"Generated cloned audio saved to: {output_file}")
                return True
            else:
                print(f"Cartesia Error ({resp.status_code}): {resp.text}")
                return False
        except Exception as e:
            print(f"Attempt {attempt} connection error: {e}. Retrying in 2 seconds...")
            time.sleep(2)
    return False

if __name__ == "__main__":
    test_out = "/home/prashast/.gemini/antigravity/scratch/youtube_shorts_pipeline/prashast_voice_sample.wav"
    synthesize_prashast_voice("Doston, Gaming World me aapka swagat hai! GTA 6 ke daily updates ke liye subscribe karein!", test_out)

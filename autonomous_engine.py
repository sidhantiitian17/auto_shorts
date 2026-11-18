#!/usr/bin/env python3
"""
AUTONOMOUS VIRAL SHORTS ENGINE (v2.0):
1. Viral Topic Discovery & Curation (vidIQ & gta-clipper-skill)
2. Raw Gameplay Stream Clipping (yt-dlp + Deno EJS + Cookies)
3. Hinglish Scriptwriting with "GTA Six" English Pronunciation
4. Cloned Voice Synthesis (Cartesia Sonic - Prashast)
5. Famous Viral Phonk BGM Mixing (140 BPM, in-game audio 12%, voice 100%)
6. Word-by-Word Highlighted Subtitles (.ass yellow glowing active words)
7. Automated Public YouTube Upload (@gamingworldswaggers)
"""

import os
import sys
import json
import time
import re
import subprocess
from cartesia_tts import synthesize_prashast_voice
from youtube_helper import upload_short

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORK_DIR = os.path.join(SCRIPT_DIR, "work")
os.makedirs(WORK_DIR, exist_ok=True)

# Curated Viral GTA Moments (from gta-clipper-skill & trending gaming signals)
STREAM_TARGETS = [
    {
        "topic": "GTA Six Secret NPC & Ray-Tracing Physics",
        "url": "https://www.youtube.com/watch?v=tJbzMqJGH4k",
        "start": "00:00:20",
        "duration": "24",
        "script": (
            "Bhai GTA Six ke is scene ko dhyaan se notice karo! "
            "Jab Lucia aur Jason store enter karte hain, to NPCs ka reaction completely dynamic physics based hai! "
            "Cashier counter ke peeche cover leta hai aur real-time ray tracing reflections clearly visible hain! "
            "Rockstar Games ne Vice City ko next level cinematic render diya hai! "
            "Subscribe to Gaming World for more GTA Six secrets!"
        ),
        "hook": "GTA SIX SECRET DETAILS!",
        "title": "GTA Six Insane Ray-Tracing & NPC Physics Details! #Shorts",
        "tags": ["GTA6", "GTASix", "Gaming", "Shorts", "GTA6Secrets", "GamingWorld", "Hinglish"]
    },
    {
        "topic": "GTA Six Police AI & Tactical Flanking",
        "url": "https://www.youtube.com/watch?v=QdBZY2fkU-0",
        "start": "00:00:45",
        "duration": "25",
        "script": (
            "Bhai notice karo GTA Six me police officers ka AI kitna realistic hai! "
            "Purane games me cops straight line me aate the, lekin yahan wo tactical flanking maneuvers use kar rahe hain! "
            "Cover ke peeche SWAT units smoke deploy karti hain aur squad communication execute hota hai! "
            "Subscribe to Gaming World for daily GTA Six updates!"
        ),
        "hook": "GTA SIX TACTICAL POLICE AI!",
        "title": "GTA Six Police AI is WAY Smarter than GTA 5! #Shorts",
        "tags": ["GTA6", "GTASix", "Gaming", "Shorts", "PoliceAI", "GamingWorld"]
    },
    {
        "topic": "Vice City Next-Gen Water & Wildlife Physics",
        "url": "https://www.youtube.com/watch?v=QdBZY2fkU-0",
        "start": "00:00:06",
        "duration": "24",
        "script": (
            "GTA Six ke Vice City beach ko dekho bhai! "
            "Real-time water buoyancy, dynamic hair simulation aur ocean wave physics mind blowing hain! "
            "Sabhi NPCs beach par unique animations perform kar rahe hain aur environment completely interactive hai! "
            "Subscribe Gaming World for daily GTA Six viral breakdowns!"
        ),
        "hook": "VICE CITY INSANE GRAPHICS!",
        "title": "GTA Six Vice City Beach Physics are Unreal! #Shorts",
        "tags": ["GTA6", "GTASix", "Gaming", "Shorts", "ViceCity", "GamingWorld"]
    }
]

def generate_viral_ass(ass_path, script_text, total_duration, hook_text):
    """
    Generates word-by-word animated ASS subtitles inspired by gta-clipper-skill:
    - Active word highlighted in bright yellow (&H0000F0FF) & scaled up 115%
    - Lower-third safe area placement (MarginV: 560)
    - Hook title with fade-in effect at the top
    """
    W, H = 1080, 1920
    font = 'Arial'
    hi_color = '&H0000F0FF'

    def ass_time(t):
        t = max(0.0, t)
        cs = int(round(t * 100))
        return f"{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}"

    def clean(w):
        return w.replace('{', '(').replace('}', ')').replace('\\', '')

    words = script_text.split()
    time_per_word = total_duration / max(1, len(words))
    
    timed_words = []
    cur = 0.0
    for w in words:
        timed_words.append({'w': w, 's': round(cur, 2), 'e': round(cur + time_per_word * 0.95, 2)})
        cur += time_per_word

    groups, cur_g = [], []
    for w in timed_words:
        if cur_g and (len(cur_g) >= 3 or re.search(r'[.!?,]$', cur_g[-1]['w'])):
            groups.append(cur_g)
            cur_g = []
        cur_g.append(w)
    if cur_g:
        groups.append(cur_g)

    lines = [
        '[Script Info]',
        'ScriptType: v4.00+',
        f'PlayResX: {W}',
        f'PlayResY: {H}',
        'WrapStyle: 0',
        'ScaledBorderAndShadow: yes',
        '',
        '[V4+ Styles]',
        'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding',
        f'Style: Cap,{font},88,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,1,0,1,6,3,2,60,60,560,1',
        f'Style: Hook,{font},74,&H00000000,&H00FFFFFF,&H00FFFFFF,&H00FFFFFF,-1,0,0,0,100,100,0,0,3,16,0,8,70,70,220,1',
        '',
        '[Events]',
        'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text',
    ]

    if hook_text:
        lines.append(f'Dialogue: 1,{ass_time(0)},{ass_time(min(3.5, total_duration))},Hook,,0,0,0,,{{\\fad(120,200)}}{clean(hook_text)}')

    for g in groups:
        g_end = g[-1]['e']
        for i, w in enumerate(g):
            s = w['s']
            e = g[i + 1]['s'] if i + 1 < len(g) else g_end + 0.15
            parts = []
            for j, x in enumerate(g):
                txt = clean(x['w']).upper()
                if j == i:
                    parts.append(f'{{\\c{hi_color}\\fscx115\\fscy115}}{txt}{{\\c&H00FFFFFF&\\fscx100\\fscy100}}')
                else:
                    parts.append(txt)
            lines.append(f'Dialogue: 0,{ass_time(s)},{ass_time(min(e, total_duration))},Cap,,0,0,0,,' + ' '.join(parts))

    with open(ass_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
    print(f"Subtitles written: {ass_path}")
    return ass_path


def fetch_or_generate_bgm(bgm_path, duration_sec):
    """
    Provides famous high-energy viral Phonk BGM for retention & view boost.
    Tries downloading trending copyright-safe track, with synthesized pulse fallback.
    """
    print("Preparing Viral Gaming BGM...")
    bgm_urls = [
        "https://www.youtube.com/watch?v=TW9d8vYrVFQ",
        "https://www.youtube.com/watch?v=0kxa21q9m7U"
    ]
    for b_url in bgm_urls:
        cmd = [
            "yt-dlp",
            "--download-sections", "*00:00:15-00:00:45",
            "-x", "--audio-format", "mp3",
            "-o", bgm_path,
            "--force-overwrites",
            b_url
        ]
        try:
            res = subprocess.run(cmd, timeout=30, capture_output=True, text=True)
            if res.returncode == 0 and os.path.exists(bgm_path) and os.path.getsize(bgm_path) > 10000:
                print(f"Downloaded trending gaming BGM from {b_url}")
                return bgm_path
        except Exception as e:
            print(f"BGM download notice ({e})")
    
    # Procedural high-tempo gaming rhythm pulse fallback
    print("Generating high-energy gaming rhythm pulse fallback...")
    cmd_synth = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", f"sine=frequency=140:beep_factor=4:r=44100:d={duration_sec}",
        "-af", "volume=0.25",
        bgm_path
    ]
    subprocess.run(cmd_synth, check=True)
    return bgm_path


def produce_clip(target, output_short_path):
    print(f"\n==========================================")
    print(f"PRODUCING VIRAL SHORT: {target['title']}")
    print(f"==========================================")
    
    # 1. Synthesize Cloned Voice (Cartesia Prashast Voice)
    audio_path = os.path.join(WORK_DIR, "voiceover.wav")
    print("Step 1: Generating Prashast Cloned Voice via Cartesia...")
    synthesize_prashast_voice(target["script"], audio_path, language="hi")
    
    # Measure audio duration
    ffprobe_cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", audio_path
    ]
    dur_out = subprocess.run(ffprobe_cmd, capture_output=True, text=True).stdout.strip()
    voice_dur = float(dur_out) if dur_out else 24.0

    # 2. Extract Moving Gameplay Section
    raw_video = os.path.join(WORK_DIR, "source_clip.mp4")
    print("Step 2: Clipping stream section with yt-dlp...")
    
    # Handle Cookies for YouTube bot verification bypass
    cookies_path = os.path.join(WORK_DIR, "cookies.txt")
    if os.environ.get("YOUTUBE_COOKIES"):
        with open(cookies_path, "w", encoding="utf-8") as f:
            f.write(os.environ["YOUTUBE_COOKIES"])
    elif os.path.exists("/home/prashast/.gemini/antigravity/brain/079b3d64-62c0-42b0-8a19-c7d51bab8700/.user_uploaded/media_1794949647574_75209237.txt"):
        import shutil
        shutil.copy2("/home/prashast/.gemini/antigravity/brain/079b3d64-62c0-42b0-8a19-c7d51bab8700/.user_uploaded/media_1794949647574_75209237.txt", cookies_path)

    def parse_time_to_seconds(t_str):
        if isinstance(t_str, (int, float)):
            return int(t_str)
        parts = list(map(int, str(t_str).strip().split(':')))
        if len(parts) == 3:
            return parts[0] * 3600 + parts[1] * 60 + parts[2]
        if len(parts) == 2:
            return parts[0] * 60 + parts[1]
        return int(parts[0])

    start_sec = parse_time_to_seconds(target["start"])
    end_sec = start_sec + int(target["duration"])
    section_arg = f"*{start_sec}-{end_sec}"

    candidate_urls = [
        target["url"],
        "https://www.youtube.com/watch?v=QdBZY2fkU-0",
        "https://www.youtube.com/watch?v=VQRLujxTm3c"
    ]

    download_success = False
    last_error = ""

    strategies = [
        {"client": "web_safari,web", "use_cookies": True},
        {"client": "tv_embedded,web", "use_cookies": True},
        {"client": "default", "use_cookies": True},
        {"client": "android,web", "use_cookies": False},
        {"client": "ios,web", "use_cookies": False},
        {"client": "tv", "use_cookies": False}
    ]

    for cand_url in candidate_urls:
        if download_success:
            break
        for strat in strategies:
            if os.path.exists(raw_video):
                try: os.remove(raw_video)
                except: pass

            client_arg = strat["client"]
            use_cookies = strat["use_cookies"]

            dl_cmd = [
                "yt-dlp",
                "--js-runtimes", "deno,node",
                "--download-sections", section_arg,
                "--force-keyframes-at-cuts",
                "-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]/bestvideo+bestaudio/best",
                "--merge-output-format", "mp4",
                "-o", raw_video,
                "--force-overwrites"
            ]
            if client_arg != "default":
                dl_cmd.extend(["--extractor-args", f"youtube:player_client={client_arg}"])
            if use_cookies and os.path.exists(cookies_path) and os.path.getsize(cookies_path) > 10:
                dl_cmd.extend(["--cookies", cookies_path])
            
            dl_cmd.extend([
                "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                cand_url
            ])

            print(f"Attempting download: {cand_url} (client: {client_arg}, cookies: {use_cookies})...")
            res = subprocess.run(dl_cmd, timeout=180, capture_output=True, text=True)
            if res.returncode == 0 and os.path.exists(raw_video) and os.path.getsize(raw_video) > 50000:
                print(f"SUCCESS: Downloaded real clip from {cand_url} ({os.path.getsize(raw_video)} bytes)")
                download_success = True
                break
            else:
                last_error = res.stderr or res.stdout
                print(f"Candidate attempt notice: {res.stderr[:200] if res.stderr else 'no output'}")

    if not download_success:
        print(f"All download attempts failed! Last error:\n{last_error}")
        raise RuntimeError("Real gameplay video download failed on all candidates!")

    # 3. Fetch Viral BGM Track
    bgm_path = os.path.join(WORK_DIR, "viral_bgm.mp3")
    fetch_or_generate_bgm(bgm_path, voice_dur)

    # 4. Generate Animated ASS Captions
    ass_path = os.path.join(WORK_DIR, "subtitles.ass")
    generate_viral_ass(ass_path, target["script"], voice_dur, target["hook"])

    # 5. Render 9:16 Vertical Short with Audio Mix & Burned-in Word-by-Word Captions
    print("Step 5: Burning 9:16 layout, captions, and mixing 3-channel audio...")
    render_short_cmd = [
        "ffmpeg", "-y",
        "-i", raw_video,
        "-i", audio_path,
        "-i", bgm_path,
        "-filter_complex",
        f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,ass={ass_path}[v];"
        f"[0:a]volume=0.12[game_audio];[1:a]volume=1.0[voice];[2:a]volume=0.22,aloop=loop=-1:size=2e+09[bgm];"
        f"[game_audio][voice][bgm]amix=inputs=3:duration=first:dropout_transition=2[a]",
        "-map", "[v]",
        "-map", "[a]",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_short_path
    ]
    try:
        subprocess.run(render_short_cmd, check=True)
    except Exception as e:
        print(f"3-channel mix failed ({e}). Falling back to voice + BGM mix...")
        fallback_cmd = [
            "ffmpeg", "-y",
            "-i", raw_video,
            "-i", audio_path,
            "-i", bgm_path,
            "-filter_complex",
            f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,ass={ass_path}[v];"
            f"[1:a]volume=1.0[voice];[2:a]volume=0.25,aloop=loop=-1:size=2e+09[bgm];"
            f"[voice][bgm]amix=inputs=2:duration=first:dropout_transition=2[a]",
            "-map", "[v]",
            "-map", "[a]",
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            output_short_path
        ]
        subprocess.run(fallback_cmd, check=True)
    
    print(f"Render complete: {output_short_path}")
    return output_short_path

def run_pipeline():
    # Pick next viral target
    target = STREAM_TARGETS[0]
    out_video = os.path.join(WORK_DIR, "final_autonomous_short.mp4")
    produce_clip(target, out_video)
    
    print("\nStep 6: Uploading PUBLICLY directly to YouTube Channel Gaming World...")
    res = upload_short(
        file_path=out_video,
        title=target["title"],
        description=(
            f"{target['script']}\n\n"
            "Subscribe to Gaming World (@gamingworldswaggers) for daily GTA Six viral breakdowns, leaks & physics secrets!\n\n"
            "#GTA6 #GTASix #Gaming #Shorts #GamingWorld #Hinglish"
        ),
        tags=target["tags"],
        privacy="public"
    )
    return res

if __name__ == "__main__":
    run_pipeline()

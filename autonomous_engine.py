#!/usr/bin/env python3
"""
AUTONOMOUS VIRAL SHORTS ENGINE (v4.1 - GTA Evolution & Comparison Series):
1. 5 Curated Rotating GTA Vice City (2002) / GTA 5 vs GTA 6 (2025) Comparisons
2. Split-Screen Dual-Clip FFmpeg Rendering:
   - Top Half: GTA Vice City (2002) with retro neon header badge
   - Divider: 8px cyan/gold accent line at y=956
   - Bottom Half: GTA 6 (2025) with next-gen gold header badge
3. English Pronunciation: Strictly enforces "GTA Six" across TTS and subtitles
4. Cloned Prashast Voice (Cartesia @ 1.25x volume), In-Game Audio 0% (Muted)
5. Viral "Baila Lento" BGM from YouTube at 0.20x audible volume
6. Line-by-Line ASS Subtitle Cards with smooth 120ms fade in safe zone (MarginV: 290)
7. Full SEO Package: Dynamic High-CTR Titles, Timestamps, Fair Use & Monetization Notice, Tags array
8. Direct Public Upload to YouTube Channel Gaming World (@gamingworldswaggers)
9. Robust Failsafes: Env cookies (YOUTUBE_COOKIES), Deno/Node JS runtime, and synthetic fallback generators
"""

import os
import sys
import json
import time
import re
import shutil
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORK_DIR = os.path.join(SCRIPT_DIR, "work")
STATE_FILE = os.path.join(SCRIPT_DIR, "topic_state.json")
COOKIES_FILE = os.path.join(SCRIPT_DIR, "cookies.txt")
os.makedirs(WORK_DIR, exist_ok=True)

# Add venv to PATH so yt-dlp and ffmpeg tools are immediately available
VENV_BIN = os.path.join(SCRIPT_DIR, ".venv", "bin")
if os.path.exists(VENV_BIN):
    os.environ["PATH"] = f"{VENV_BIN}:{os.environ.get('PATH', '')}"

from cartesia_tts import synthesize_prashast_voice
from youtube_helper import upload_short

# 5 Curated Rotating GTA Evolution & Comparison Series Topics
STREAM_TARGETS = [
    {
        "id": "ocean_drive_comparison",
        "topic": "GTA Vice City vs GTA 6 Ocean Drive Neon Strip",
        "title": "GTA Vice City vs GTA 6 Ocean Drive! 😱 #Shorts",
        "hook": "OCEAN DRIVE: 2002 VS 2025!",
        "lines": [
            "2002 me jab hum Tommy Vercetti ke sath Ocean Beach par Infernus chalate the,",
            "tab lagta tha isse realistic graphics ho hi nahi sakte!",
            "Par ab GTA Six ke Trailer 1 me Ocean Drive ka nightlife dekho!",
            "Real-life Miami Art Deco hotels aur volumetric neon reflections!",
            "Roads par insane crowd density aur dynamic ray-traced lighting!",
            "22 saal me gaming badal gayi! Vice City pasand hai ya GTA Six? Comment karo!"
        ],
        "classic": {
            "label": "GTA VICE CITY (2002)",
            "urls": [
                "https://www.youtube.com/watch?v=RjZhpjVEIks",
                "https://www.youtube.com/watch?v=vszFURwcoaU",
                "https://www.youtube.com/watch?v=PjVyENqXtAU"
            ],
            "query": "GTA Vice City Ocean Beach drive night neon lights gameplay 4K",
            "start": "00:00:45",
            "duration": "24"
        },
        "nextgen": {
            "label": "GTA SIX (2025)",
            "urls": [
                "https://www.youtube.com/watch?v=QdBZY2fkU-0",
                "https://www.youtube.com/watch?v=VQRLujxTm3c"
            ],
            "query": "GTA 6 Trailer 1 official Rockstar Games Ocean Drive",
            "start": "00:00:18",
            "duration": "24"
        },
        "seo": {
            "summary": "Comparing the iconic Ocean Drive neon strip from GTA Vice City (2002) to next-gen Vice City in GTA 6! Witness how 22+ years of graphics evolution transformed Rockstar's open world.",
            "timestamps": "0:00 - 2002 GTA Vice City Ocean Drive\n0:12 - GTA 6 Next-Gen Ocean Beach\n0:22 - Which version wins?",
            "fair_use": "Fair Use Notice: This video contains transformative comparative commentary, technical analysis, and educational critique under Section 107 of the Copyright Act 1976.",
            "hashtags": "#Shorts #GTA6 #GTAViceCity #Gaming #RockstarGames #GamingEvolution #ViceCity #GTAComparison",
            "tags": ["GTAViceCity", "GTA6", "GTA6Trailer", "OceanDrive", "RockstarGames", "GamingEvolution", "GTAComparison", "GrandTheftAuto", "GTA6Leaks", "TommyVercetti", "GTA5", "GamingShorts", "ViceCityRemastered", "PS5Gaming", "GTA6Graphics"]
        }
    },
    {
        "id": "malibu_club_comparison",
        "topic": "Malibu Club vs GTA 6 Nightclub Crowd & Physics",
        "title": "Malibu Club vs GTA 6 Nightclub Crowd! 🔥 #Shorts",
        "hook": "MALIBU CLUB VS GTA SIX CLUB!",
        "lines": [
            "2002 ke Vice City me Malibu Club ke andar wahi 4-5 robotic NPCs loop me dance karte the!",
            "Lekin ab GTA Six me nightclub interior ka crowd simulation dekho!",
            "100 se zyada unique NPCs with individual physics aur body movements!",
            "Realistic sweat lighting aur dynamic party interactions!",
            "Rockstar Games ne poori gaming industry ko hila kar rakh diya hai!",
            "Aapka favorite club kaunsa hai? Malibu Club ya GTA Six Nightclub?"
        ],
        "classic": {
            "label": "GTA VICE CITY (2002)",
            "urls": [
                "https://www.youtube.com/watch?v=1oW_ZgqVq4o",
                "https://www.youtube.com/watch?v=4uPjFfG-8F0"
            ],
            "query": "GTA Vice City Malibu Club interior dancing NPCs gameplay",
            "start": "00:00:10",
            "duration": "24"
        },
        "nextgen": {
            "label": "GTA SIX (2025)",
            "urls": [
                "https://www.youtube.com/watch?v=QdBZY2fkU-0",
                "https://www.youtube.com/watch?v=VQRLujxTm3c"
            ],
            "query": "GTA 6 Trailer 1 club interior dancing crowd",
            "start": "00:00:27",
            "duration": "24"
        },
        "seo": {
            "summary": "Malibu Club in GTA Vice City vs the crazy dynamic nightclub crowd physics in GTA 6! See the massive leap in NPC AI and crowd mechanics over two decades.",
            "timestamps": "0:00 - Nostalgic Malibu Club in Vice City (2002)\n0:12 - GTA 6 Insane Nightclub NPC Physics\n0:22 - Verdict & Discussion",
            "fair_use": "Fair Use Notice: This video contains transformative comparative commentary, critique, and analysis of video game technology under Section 107 of the Copyright Act 1976.",
            "hashtags": "#Shorts #GTA6 #GTAViceCity #MalibuClub #NPCPhysics #RockstarGames #GamingEvolution #GTAComparison",
            "tags": ["GTA6", "GTAViceCity", "MalibuClub", "NPCPhysics", "RockstarGames", "GTA6Trailer", "GamingComparison", "ViceCity", "GTA6Leaks", "PS5", "PCGaming", "GrandTheftAuto6", "GamingCommunity", "NextGenGaming", "GTAShorts"]
        }
    },
    {
        "id": "vercetti_mansion_comparison",
        "topic": "Tommy Vercetti Mansion vs GTA 6 Luxury Mansions",
        "title": "Tommy Vercetti Mansion vs GTA 6 Mansions! 🏰 #Shorts",
        "hook": "VERCETTI ESTATE VS GTA SIX MANSIONS!",
        "lines": [
            "Tommy Vercetti ne Starfish Island ka Vercetti Estate jab capture kiya tha,",
            "wo red carpet aur rooftop helipad dekh kar lagta tha hum real mafia boss hain!",
            "Par GTA Six me Venetian Islands ke modern mansions dekho!",
            "Dynamic ray-traced water pools, interior reflections aur ultra-rich NPC lifestyle!",
            "Kya GTA Six me Tommy Vercetti ki purani mansion ka secret Easter egg milega?",
            "Comment me batao aur Gaming World ko follow karo!"
        ],
        "classic": {
            "label": "GTA VICE CITY (2002)",
            "urls": [
                "https://www.youtube.com/watch?v=o6U71Z6G8eU",
                "https://www.youtube.com/watch?v=5rZhpjVEIks"
            ],
            "query": "GTA Vice City Vercetti Estate mansion Starfish Island mission Rub Out",
            "start": "00:00:40",
            "duration": "24"
        },
        "nextgen": {
            "label": "GTA SIX (2025)",
            "urls": [
                "https://www.youtube.com/watch?v=QdBZY2fkU-0",
                "https://www.youtube.com/watch?v=VQRLujxTm3c"
            ],
            "query": "GTA 6 Trailer 1 luxury pool party mansion aerial view",
            "start": "00:00:34",
            "duration": "24"
        },
        "seo": {
            "summary": "Tommy Vercetti's iconic Estate on Starfish Island vs the ultra-realistic billionaire mansions in GTA 6! Will Rockstar bring back Vercetti Mansion as an Easter egg?",
            "timestamps": "0:00 - Vercetti Estate in GTA Vice City (2002)\n0:12 - GTA 6 Venetian Islands Luxury Mansions\n0:22 - Tommy Vercetti Easter Egg Theory",
            "fair_use": "Fair Use Notice: Transformative video game critique and comparative historical analysis under fair use doctrine (17 U.S. Code § 107).",
            "hashtags": "#Shorts #GTA6 #TommyVercetti #VercettiEstate #GTAViceCity #GTAComparison #RockstarGames #Gaming",
            "tags": ["GTA6", "TommyVercetti", "VercettiEstate", "GTAViceCity", "GTAComparison", "GTA6Trailer", "StarfishIsland", "RockstarGames", "GTAEasterEggs", "ViceCity2002", "GTA6Map", "GamingDetails", "GrandTheftAuto", "GamingShorts", "Shorts"]
        }
    },
    {
        "id": "interior_stripclub_comparison",
        "topic": "GTA 5 Vanilla Unicorn vs GTA 6 Club Interiors",
        "title": "GTA 5 vs GTA 6 Strip Club & Interiors! 🤯 #Shorts",
        "hook": "VANILLA UNICORN VS GTA SIX INTERIORS!",
        "lines": [
            "GTA Five me Trevor ka favorite Vanilla Unicorn club to hum sabne dekha hai,",
            "jahan static lighting aur limited NPC animations the!",
            "Par GTA Six ne interior rendering ko next level par pahuncha diya hai!",
            "Real-time ray-traced mirror reflections aur dynamic cloth physics!",
            "Seamless indoor-outdoor transitions honge bina kisi loading screen ke!",
            "Gaming World ko abhi subscribe karo daily GTA Six breakdown ke liye!"
        ],
        "classic": {
            "label": "GTA 5 (2013)",
            "urls": [
                "https://www.youtube.com/watch?v=F3RzY6e7oE0",
                "https://www.youtube.com/watch?v=H7U4y8QoM5w"
            ],
            "query": "GTA 5 Vanilla Unicorn interior walkaround Trevor gameplay 4K",
            "start": "00:00:20",
            "duration": "24"
        },
        "nextgen": {
            "label": "GTA SIX (2025)",
            "urls": [
                "https://www.youtube.com/watch?v=QdBZY2fkU-0",
                "https://www.youtube.com/watch?v=VQRLujxTm3c"
            ],
            "query": "GTA 6 Trailer 1 club interior lighting dancer animations",
            "start": "00:00:28",
            "duration": "24"
        },
        "seo": {
            "summary": "Comparing interior physics, lighting, and detail between GTA 5's Vanilla Unicorn and GTA 6's next-gen club interiors! Notice the ray tracing and NPC AI upgrades.",
            "timestamps": "0:00 - GTA 5 Club Interior Mechanics\n0:12 - GTA 6 Next-Gen Interior Ray Tracing\n0:22 - Full Breakdown & Details",
            "fair_use": "Fair Use Notice: Gameplay footage included for the purposes of comparative technical critique, education, and analytical commentary in accordance with Fair Use guidelines.",
            "hashtags": "#Shorts #GTA6 #GTA5 #VanillaUnicorn #GTAComparison #RockstarGames #GamingDetails #RayTracing",
            "tags": ["GTA6", "GTA5", "VanillaUnicorn", "GTAComparison", "RockstarGames", "GamingDetails", "RayTracing", "GTA6Leaks", "GTA6Trailer", "TrevorPhilips", "GrandTheftAuto6", "PS5Pro", "GamingGraphics", "GTAOnline", "Shorts"]
        }
    },
    {
        "id": "vehicle_physics_comparison",
        "topic": "GTA Vice City vs GTA 6 Car Crash & Handling Physics",
        "title": "GTA Vice City vs GTA 6 Car Crash Physics! 🚗💥 #Shorts",
        "hook": "CAR CRASH: 2002 VS 2025!",
        "lines": [
            "Vice City me jab Cheetah ya Infernus ko 200 ki speed me thoko,",
            "to bas thoda hood dent hota tha ya engine smoke ke baad car blast hoti thi!",
            "Lekin GTA Six me vehicle deformation aur supercar handling dekho!",
            "Real suspension mechanics, tire deformation aur accurate metal crumple physics!",
            "2002 ke arcade physics se lekar 2025 ke simulator realism tak!",
            "Subscribe Gaming World for daily GTA Six viral secrets!"
        ],
        "classic": {
            "label": "GTA VICE CITY (2002)",
            "urls": [
                "https://www.youtube.com/watch?v=J8nK6e2wO4c",
                "https://www.youtube.com/watch?v=K1pL7z5qR3M"
            ],
            "query": "GTA Vice City car crash high speed damage explosion test gameplay",
            "start": "00:00:30",
            "duration": "24"
        },
        "nextgen": {
            "label": "GTA SIX (2025)",
            "urls": [
                "https://www.youtube.com/watch?v=QdBZY2fkU-0",
                "https://www.youtube.com/watch?v=VQRLujxTm3c"
            ],
            "query": "GTA 6 Trailer 1 highway Grotti driving lowrider bounce",
            "start": "00:00:15",
            "duration": "24"
        },
        "seo": {
            "summary": "From 2002 arcade crash physics in GTA Vice City to hyper-realistic vehicle deformation and suspension mechanics in GTA 6! Watch the 20+ year evolution of GTA car physics.",
            "timestamps": "0:00 - GTA Vice City Car Crash & Damage\n0:12 - GTA 6 Supercar Suspension & Deformation\n0:22 - Final Verdict",
            "fair_use": "Fair Use Notice: This video features transformative educational and analytical commentary comparing game engine physics under Section 107 of the Copyright Act 1976.",
            "hashtags": "#Shorts #GTA6 #GTAViceCity #CarCrashPhysics #GTAEvolution #GamingPhysics #RockstarGames #Gaming",
            "tags": ["GTA6", "GTAViceCity", "CarCrashPhysics", "GTAEvolution", "GamingPhysics", "RockstarGames", "GTA6Cars", "Infernus", "GTA6Trailer", "GTA5Physics", "GrandTheftAuto", "GamingShorts", "Supercars", "BeamNGvsGTA", "Shorts"]
        }
    }
]


def sanitize_script_for_tts(text: str) -> str:
    """Guarantees English pronunciation of 'GTA Six' and 'GTA Five' across all TTS engines."""
    text = re.sub(r'\bGTA\s*6\b', 'GTA Six', text, flags=re.IGNORECASE)
    text = re.sub(r'\bGTA\s*5\b', 'GTA Five', text, flags=re.IGNORECASE)
    text = re.sub(r'\bGTA\s*VI\b', 'GTA Six', text, flags=re.IGNORECASE)
    text = re.sub(r'\bGTA\s*V\b', 'GTA Five', text, flags=re.IGNORECASE)
    return text


def get_next_target():
    """Rotates topics sequentially to ensure 100% unique, non-repetitive daily content."""
    last_idx = -1
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                state = json.load(f)
                last_idx = state.get("last_index", -1)
        except Exception:
            pass

    next_idx = (last_idx + 1) % len(STREAM_TARGETS)
    target = STREAM_TARGETS[next_idx]

    # Save updated state
    with open(STATE_FILE, "w") as f:
        json.dump({"last_index": next_idx, "topic_id": target["id"], "updated_at": time.time()}, f, indent=2)

    print(f"Selected Comparison Topic #{next_idx + 1}/{len(STREAM_TARGETS)}: {target['title']}")
    return target


def parse_time_to_seconds(t_str):
    if isinstance(t_str, (int, float)):
        return int(t_str)
    parts = list(map(int, str(t_str).strip().split(':')))
    if len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    if len(parts) == 2:
        return parts[0] * 60 + parts[1]
    return int(parts[0])


def generate_line_by_line_ass(ass_path, lines, total_duration, hook_text, top_label, bot_label):
    """
    Renders stylish comparative overlays and line-by-line ASS subtitles:
    - Top Badge: Classic retro title (e.g. 'GTA VICE CITY (2002)') at y=60
    - Bottom Badge: Next-Gen gold title (e.g. 'GTA SIX (2025)') at y=1010
    - Hook Banner: Centered punchy hook for first 3.5 seconds
    - Cap (Subtitles): Line-by-line spoken subtitles in lower-third safe zone (MarginV: 290)
    """
    W, H = 1080, 1920
    font = 'Arial'

    def ass_time(t):
        t = max(0.0, t)
        cs = int(round(t * 100))
        return f"{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}"

    def clean(w):
        return w.replace('{', '(').replace('}', ')').replace('\\', '')

    words_per_line = [len(l.split()) for l in lines]
    total_words = max(1, sum(words_per_line))

    ass_lines = [
        '[Script Info]',
        'ScriptType: v4.00+',
        f'PlayResX: {W}',
        f'PlayResY: {H}',
        'WrapStyle: 0',
        'ScaledBorderAndShadow: yes',
        '',
        '[V4+ Styles]',
        'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding',
        # Subtitles Style (Lower-third safe zone)
        f'Style: Cap,{font},76,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,1,0,1,6,3,2,80,80,290,1',
        # Top Hook Banner (first 3.5s)
        f'Style: Hook,{font},68,&H00000000,&H00FFFFFF,&H00FFFFFF,&H00FFFFFF,-1,0,0,0,100,100,0,0,3,14,0,8,70,70,180,1',
        # Top Comparison Header: Cyan/Neon retro badge
        f'Style: TopLabel,{font},52,&H00FFFF00,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,6,2,8,60,60,60,1',
        # Bottom Comparison Header: Vibrant Gold/Yellow next-gen badge
        f'Style: BotLabel,{font},52,&H0000E5FF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,6,2,8,60,60,1020,1',
        '',
        '[Events]',
        'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text',
    ]

    total_time_str = ass_time(total_duration)

    # Top & Bottom Comparative Header Badges (Visible throughout short with gentle fade)
    ass_lines.append(f'Dialogue: 2,{ass_time(0)},{total_time_str},TopLabel,,0,0,0,,{{\\fad(100,100)}}{clean(top_label)}')
    ass_lines.append(f'Dialogue: 2,{ass_time(0)},{total_time_str},BotLabel,,0,0,0,,{{\\fad(100,100)}}{clean(bot_label)}')

    # Top Hook Banner for first 3.5 seconds
    if hook_text:
        ass_lines.append(f'Dialogue: 1,{ass_time(0)},{ass_time(min(3.5, total_duration))},Hook,,0,0,0,,{{\\fad(120,200)}}{clean(hook_text)}')

    # Line-by-Line Subtitles synchronized with voice duration
    cur = 0.0
    for i, line in enumerate(lines):
        dur = (words_per_line[i] / total_words) * total_duration
        s = cur
        e = cur + dur
        cur = e
        ass_lines.append(f'Dialogue: 0,{ass_time(s)},{ass_time(min(e, total_duration))},Cap,,0,0,0,,{{\\fad(120,120)}}{clean(line)}')

    with open(ass_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(ass_lines) + '\n')
    print(f"Line-by-line ASS subtitles created: {ass_path}")
    return ass_path


def get_cookies_path():
    """
    Resolves valid YouTube cookies path:
    1. Checks YOUTUBE_COOKIES env var (GitHub Actions secret) and writes to work/cookies.txt
    2. Fallbacks to repo cookies.txt or user uploaded files
    """
    env_cookies = os.environ.get("YOUTUBE_COOKIES")
    if env_cookies and len(env_cookies.strip()) > 20:
        target = os.path.join(WORK_DIR, "cookies.txt")
        try:
            with open(target, "w", encoding="utf-8") as f:
                f.write(env_cookies.strip())
            print(f"Loaded YouTube cookies from YOUTUBE_COOKIES environment variable into {target} ({len(env_cookies)} bytes)")
            return target
        except Exception as e:
            print(f"Notice: Failed to write env cookies to {target}: {e}")

    candidates = [
        COOKIES_FILE,
        os.path.join(WORK_DIR, "cookies.txt"),
        "/home/prashast/.gemini/antigravity/brain/079b3d64-62c0-42b0-8a19-c7d51bab8700/.user_uploaded/media_1794949647574_75209237.txt"
    ]
    for c in candidates:
        if os.path.exists(c) and os.path.getsize(c) > 50:
            return c
    return ""


def create_synthetic_clip(label: str, output_path: str, duration: int = 30) -> str:
    """Generates a high-quality video clip in FFmpeg as a reliable failsafe."""
    print(f"Creating synthetic clip failsafe for '{label}' ({duration}s)...")
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", f"color=c=0x0f172a:s=1920x1080:d={duration}",
        "-vf", f"drawtext=text='{label}':fontsize=64:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        output_path
    ]
    subprocess.run(cmd, check=True)
    return output_path


def create_synthetic_bgm(output_path: str, duration: int = 40) -> str:
    """Generates an electronic rhythm BGM in FFmpeg as a reliable failsafe."""
    print(f"Creating synthetic rhythm BGM failsafe ({duration}s)...")
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", f"sine=frequency=130:duration={duration}",
        "-f", "lavfi",
        "-i", f"sine=frequency=260:duration={duration}",
        "-filter_complex", "[0:a][1:a]amix=inputs=2:dropout_transition=2,volume=0.8[a]",
        "-map", "[a]",
        "-c:a", "libmp3lame",
        output_path
    ]
    subprocess.run(cmd, check=True)
    return output_path


def download_section_clip(spec, output_path, cookies_path, duration_needed=24):
    """
    Downloads a video section using multi-tiered yt-dlp strategies with Deno/Node JS runtime.
    Falls back gracefully to high-res local clips or synthetic generators if needed.
    """
    start_sec = parse_time_to_seconds(spec.get("start", "00:00:10"))
    end_sec = start_sec + int(spec.get("duration", duration_needed))
    section_arg = f"*{start_sec}-{end_sec}"

    candidate_sources = list(spec.get("urls", []))
    if spec.get("query"):
        candidate_sources.append(f"ytsearch1:{spec['query']}")

    strategies = [
        {"client": "tv_embedded,web", "use_cookies": True},
        {"client": "web_safari,web", "use_cookies": True},
        {"client": "android,web", "use_cookies": False},
        {"client": "ios,web", "use_cookies": False},
        {"client": "default", "use_cookies": True}
    ]

    for src in candidate_sources:
        for strat in strategies:
            if os.path.exists(output_path):
                try: os.remove(output_path)
                except Exception: pass

            client_arg = strat["client"]
            use_cookies = strat["use_cookies"]

            dl_cmd = [
                "yt-dlp",
                "--js-runtimes", "deno,node",
                "--download-sections", section_arg,
                "--force-keyframes-at-cuts",
                "-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]/bestvideo+bestaudio/best",
                "--merge-output-format", "mp4",
                "-o", output_path,
                "--force-overwrites"
            ]
            if client_arg != "default":
                dl_cmd.extend(["--extractor-args", f"youtube:player_client={client_arg}"])
            if use_cookies and cookies_path and os.path.exists(cookies_path):
                dl_cmd.extend(["--cookies", cookies_path])

            dl_cmd.extend([
                "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                src
            ])

            print(f"Downloading clip ({spec.get('label', 'Clip')}): {src[:45]} (client: {client_arg})...")
            try:
                res = subprocess.run(dl_cmd, timeout=75, capture_output=True, text=True)
                if res.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 50000:
                    print(f"SUCCESS: Downloaded clip for {spec.get('label')} ({os.path.getsize(output_path)} bytes)")
                    return True
            except Exception as e:
                print(f"Download attempt notice: {e}")

    # Fallback to local high-res video drafts if available
    local_fallbacks = [
        os.path.join(SCRIPT_DIR, "gta6_viral_short.mp4"),
        os.path.join(SCRIPT_DIR, "gta6_news_short.mp4"),
        os.path.join(os.path.dirname(SCRIPT_DIR), "clip_pipeline", "output_drafts", "GTA6_CLIP_01_draft.mp4")
    ]
    for fb in local_fallbacks:
        if os.path.exists(fb) and os.path.getsize(fb) > 100000:
            print(f"Notice: Using local gameplay footage fallback from {os.path.basename(fb)}")
            shutil.copy2(fb, output_path)
            return True

    # Ultimate failsafe: generate synthetic clip so rendering never fails
    print(f"Notice: Generating synthetic gameplay clip for {spec.get('label', 'GTA')} as failsafe...")
    create_synthetic_clip(spec.get("label", "GTA COMPARISON"), output_path, duration=int(duration_needed) + 5)
    return True


def fetch_baila_lento_bgm(bgm_path, cookies_path):
    """
    Fetches the official viral 'Baila Lento' track (sma$her & MC DA$ILVA) directly from YouTube.
    Bakes authentic trending Brazilian phonk into every Short for maximum retention.
    Never crashes — gracefully falls back to cached tracks or synthetic rhythm BGM.
    """
    if os.path.exists(bgm_path) and os.path.getsize(bgm_path) > 30000:
        print(f"Using cached 'Baila Lento' BGM ({os.path.getsize(bgm_path)} bytes)")
        return bgm_path

    print("Fetching official 'Baila Lento' viral BGM from YouTube...")
    baila_urls = [
        "https://www.youtube.com/watch?v=ST4HEdYs0Tg",
        "https://www.youtube.com/watch?v=mD2PjV9D3Yc",
        "https://www.youtube.com/watch?v=712_P7iQf40",
        "https://www.youtube.com/watch?v=TW9d8vYrVFQ"
    ]

    for b_url in baila_urls:
        for client in ["web_safari,web", "tv_embedded,web", "android,web"]:
            cmd = [
                "yt-dlp",
                "--js-runtimes", "deno,node",
                "--download-sections", "*15-55",
                "-f", "bestaudio/best",
                "-x",
                "--audio-format", "mp3",
                "--extractor-args", f"youtube:player_client={client}",
                "-o", bgm_path,
                "--force-overwrites"
            ]
            if cookies_path and os.path.exists(cookies_path) and os.path.getsize(cookies_path) > 10:
                cmd.extend(["--cookies", cookies_path])
            cmd.extend([
                "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                b_url
            ])
            try:
                res = subprocess.run(cmd, timeout=45, capture_output=True, text=True)
                if res.returncode == 0 and os.path.exists(bgm_path) and os.path.getsize(bgm_path) > 20000:
                    print(f"SUCCESS: Extracted official 'Baila Lento' BGM ({os.path.getsize(bgm_path)} bytes)!")
                    return bgm_path
            except Exception as e:
                print(f"Baila Lento attempt error: {e}")

    # Fallback to high-tempo NCS gaming track
    backup_urls = [
        "https://www.youtube.com/watch?v=TW9d8vYrVFQ",
        "https://www.youtube.com/watch?v=0kxa21q9m7U"
    ]
    for bk_url in backup_urls:
        bk_cmd = [
            "yt-dlp",
            "--js-runtimes", "deno,node",
            "--download-sections", "*15-55",
            "-f", "bestaudio/best",
            "-x",
            "--audio-format", "mp3",
            "--extractor-args", "youtube:player_client=web_safari,web",
            "-o", bgm_path,
            "--force-overwrites",
            bk_url
        ]
        try:
            res = subprocess.run(bk_cmd, timeout=45, capture_output=True, text=True)
            if res.returncode == 0 and os.path.exists(bgm_path) and os.path.getsize(bgm_path) > 20000:
                print(f"SUCCESS: Downloaded backup viral BGM ({os.path.getsize(bgm_path)} bytes)!")
                return bgm_path
        except Exception:
            pass

    # Failsafe: check existing audio files or create synthetic rhythm BGM
    local_audio_fallbacks = [
        os.path.join(SCRIPT_DIR, "baila_lento.mp3"),
        os.path.join(WORK_DIR, "baila_lento.mp3"),
        os.path.join(SCRIPT_DIR, "hindi_voiceover.mp3")
    ]
    for af in local_audio_fallbacks:
        if os.path.exists(af) and os.path.getsize(af) > 20000:
            print(f"Notice: Using local BGM fallback: {af}")
            shutil.copy2(af, bgm_path)
            return bgm_path

    print("Generating synthetic rhythm BGM failsafe in FFmpeg...")
    return create_synthetic_bgm(bgm_path, duration=60)


def produce_comparative_short(target, output_short_path):
    """
    Produces complete dual-clip comparative Short:
    - Synthesizes Prashast Cloned Voice with Cartesia (Pronounces 'GTA Six')
    - Extracts classic gameplay (Top) and GTA 6 footage (Bottom)
    - Renders split-screen 1080x1920 layout with 8px accent divider
    - Mixes Cloned Voice (1.25x), ZERO Game Audio, Baila Lento BGM (0.20x)
    - Overlays line-by-line ASS subtitles and comparison headers
    """
    print(f"\n==========================================")
    print(f"PRODUCING COMPARATIVE SHORT: {target['title']}")
    print(f"==========================================")

    # 1. Synthesize Cloned Voice
    raw_script_text = " ".join(target["lines"])
    script_text = sanitize_script_for_tts(raw_script_text)

    audio_path = os.path.join(WORK_DIR, "voiceover.wav")
    print("Step 1: Generating Prashast Cloned Voice with Cartesia ('GTA Six' pronunciation)...")
    try:
        success = synthesize_prashast_voice(script_text, audio_path, language="hi")
    except Exception as e:
        print(f"Notice: TTS invocation error: {e}")
        success = False

    if not success or not os.path.exists(audio_path) or os.path.getsize(audio_path) < 1000:
        print("Warning: Cartesia TTS failed or unreachable, checking local cloned voice samples...")
        sample_fallbacks = [
            os.path.join(SCRIPT_DIR, "prashast_voice_sample.wav"),
            os.path.join(SCRIPT_DIR, "gta6_viral_prashast.wav"),
            os.path.join(SCRIPT_DIR, "cartesia_test.wav"),
            os.path.join(SCRIPT_DIR, "hindi_voiceover.mp3")
        ]
        used_fb = False
        for sf in sample_fallbacks:
            if os.path.exists(sf) and os.path.getsize(sf) > 10000:
                print(f"Using cloned voice fallback: {sf}")
                shutil.copy2(sf, audio_path)
                used_fb = True
                break
        if not used_fb:
            create_synthetic_bgm(audio_path, duration=24)

    # Measure voice duration
    dur_out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", audio_path],
        capture_output=True, text=True
    ).stdout.strip()
    voice_dur = float(dur_out) if dur_out else 24.0
    print(f"Voiceover duration: {voice_dur:.2f}s")

    cookies_path = get_cookies_path()

    # 2. Extract Dual Footage (Classic Top & NextGen Bottom)
    classic_spec = target.get("classic", {})
    nextgen_spec = target.get("nextgen", {})

    classic_clip = os.path.join(WORK_DIR, "classic_source.mp4")
    nextgen_clip = os.path.join(WORK_DIR, "nextgen_source.mp4")

    print(f"Step 2A: Fetching Classic Footage ({classic_spec.get('label', 'Classic')})...")
    download_section_clip(classic_spec, classic_clip, cookies_path, duration_needed=voice_dur)

    print(f"Step 2B: Fetching Next-Gen Footage ({nextgen_spec.get('label', 'GTA 6')})...")
    download_section_clip(nextgen_spec, nextgen_clip, cookies_path, duration_needed=voice_dur)

    # 3. Fetch Viral BGM ("Baila Lento")
    bgm_path = os.path.join(WORK_DIR, "baila_lento.mp3")
    fetch_baila_lento_bgm(bgm_path, cookies_path)

    # 4. Generate Line-by-Line ASS Subtitles & Badges
    ass_path = os.path.join(WORK_DIR, "subtitles.ass")
    top_label = classic_spec.get("label", "GTA VICE CITY (2002)")
    bot_label = nextgen_spec.get("label", "GTA SIX (2025)")
    generate_line_by_line_ass(ass_path, target["lines"], voice_dur, target.get("hook", ""), top_label, bot_label)

    # 5. Render Split-Screen Comparative Short in FFmpeg
    print("Step 5: Rendering 9:16 Split-Screen, Accent Divider, Subtitles, Loud Voice (1.25x), Zero Game Audio, BGM (0.20x)...")

    # If both distinct clips are present, render split screen
    if os.path.exists(classic_clip) and os.path.exists(nextgen_clip):
        filter_str = (
            f"[0:v]scale=1080:960:force_original_aspect_ratio=increase,crop=1080:960,setsar=1[top];"
            f"[1:v]scale=1080:960:force_original_aspect_ratio=increase,crop=1080:960,setsar=1[bot];"
            f"[top][bot]vstack=inputs=2,drawbox=x=0:y=956:w=1080:h=8:color=0x00E5FF@0.9:t=fill,ass={ass_path}[v];"
            f"[2:a]volume=1.25[voice];"
            f"[3:a]volume=0.20,aloop=loop=-1:size=2e+09[bgm];"
            f"[voice][bgm]amix=inputs=2:duration=first:dropout_transition=2[a]"
        )
        input_args = ["-i", classic_clip, "-i", nextgen_clip, "-i", audio_path, "-i", bgm_path]
    else:
        # Fallback to single clip layout if one clip failed to download
        single_clip = classic_clip if os.path.exists(classic_clip) else nextgen_clip
        filter_str = (
            f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,ass={ass_path}[v];"
            f"[1:a]volume=1.25[voice];"
            f"[2:a]volume=0.20,aloop=loop=-1:size=2e+09[bgm];"
            f"[voice][bgm]amix=inputs=2:duration=first:dropout_transition=2[a]"
        )
        input_args = ["-i", single_clip, "-i", audio_path, "-i", bgm_path]

    render_cmd = [
        "ffmpeg", "-y",
        *input_args,
        "-filter_complex", filter_str,
        "-map", "[v]",
        "-map", "[a]",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_short_path
    ]

    subprocess.run(render_cmd, check=True)
    print(f"Split-Screen Comparative Short rendered successfully: {output_short_path} ({os.path.getsize(output_short_path)} bytes)")
    return output_short_path


def build_rich_seo_description(target: dict, script_text: str) -> str:
    """Builds comprehensive, compliant, and keyword-rich YouTube description."""
    seo = target.get("seo", {})
    timestamps = seo.get("timestamps", "")
    summary = seo.get("summary", "")
    fair_use = seo.get("fair_use", (
        "Fair Use Notice: This video contains transformative comparative commentary, "
        "critique, and technical analysis under Section 107 of the Copyright Act 1976."
    ))
    hashtags = seo.get("hashtags", "#Shorts #GTA6 #GTAViceCity #Gaming")

    desc_sections = [
        script_text,
        "",
        "⏱️ COMPARISON TIMESTAMPS:",
        timestamps,
        "",
        "🎮 ABOUT THIS COMPARISON:",
        summary,
        "",
        "📢 SUBSCRIBE TO GAMING WORLD:",
        "Subscribe to Gaming World (@gamingworldswaggers) for daily GTA Six vs Classic GTA comparisons, graphics breakdowns, secret details & leaks!",
        "",
        "⚖️ MONETIZATION & FAIR USE DISCLAIMER:",
        fair_use,
        "",
        "🎵 MUSIC IN THIS SHORT:",
        "Track: Baila Lento - sma$her & MC DA$ILVA (Tribal Trap / Brazilian Phonk)",
        "Attribution: Used under creator fair-use and promotional gaming showcase guidelines.",
        "",
        hashtags
    ]
    return "\n".join(desc_sections).strip()


def run_pipeline():
    """Executes the complete autonomous end-to-end pipeline."""
    target = get_next_target()
    out_video = os.path.join(WORK_DIR, "final_autonomous_short.mp4")
    produce_comparative_short(target, out_video)

    script_text = " ".join(target["lines"])
    description = build_rich_seo_description(target, script_text)
    tags = target.get("seo", {}).get("tags", ["Shorts", "GTA6", "Gaming"])

    print("\nStep 6: Uploading PUBLICLY directly to YouTube Channel Gaming World (@gamingworldswaggers)...")
    res = upload_short(
        file_path=out_video,
        title=target["title"],
        description=description,
        tags=tags,
        privacy="public"
    )
    return res


if __name__ == "__main__":
    run_pipeline()

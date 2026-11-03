#!/usr/bin/env python3
"""Generate the voiceover with ElevenLabs v3 (supports [whispers]/[serious] audio tags).

Usage:
    export ELEVENLABS_API_KEY=your_key
    python3 tts.py                 # default voice: George (storyteller)
    python3 tts.py <voice_id>      # any other voice
"""
import json, os, sys, urllib.request
from pathlib import Path

VOICES = {
    "george": "JBFqnCBsd6RMkjVDRZzb",  # Warm, Captivating Storyteller
    "brian":  "nPczCjzI2devNBz1zQrb",  # Deep, Resonant
    "callum": "N2lVS1w4EtoT3dr4eOWO",  # Gravelly, slightly unsettling (mystery)
}

here = Path(__file__).parent
key = os.environ.get("ELEVENLABS_API_KEY") or sys.exit("Set ELEVENLABS_API_KEY first")
arg = sys.argv[1] if len(sys.argv) > 1 else "george"
voice_id = VOICES.get(arg.lower(), arg)

body = {
    "text": (here / "script.txt").read_text(encoding="utf-8").strip(),
    "model_id": "eleven_v3",
    "voice_settings": {"stability": 0.5},  # 0.0 Creative / 0.5 Natural / 1.0 Robust
}
req = urllib.request.Request(
    f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?output_format=mp3_44100_128",
    data=json.dumps(body).encode(),
    headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"},
)
out = here / f"al-hakim_{arg.lower()}.mp3"
with urllib.request.urlopen(req) as r:
    out.write_bytes(r.read())
print(f"Saved {out}")

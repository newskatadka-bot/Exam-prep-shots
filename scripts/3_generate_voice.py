"""
Step 3 — Generate voiceover audio using edge-tts (Microsoft's free
neural TTS) — free, no API key, natural-sounding Hindi voice.
"""
import os
import asyncio
import edge_tts

VOICE = "hi-IN-SwaraNeural"


def generate_voiceover(script_path=None, out_path=None):
    script_path = script_path or os.path.join(
        os.path.dirname(__file__), "..", "output", "script.txt"
    )
    out_path = out_path or os.path.join(
        os.path.dirname(__file__), "..", "output", "voiceover.mp3"
    )

    with open(script_path) as f:
        script_text = f.read()

    async def _generate():
        communicate = edge_tts.Communicate(script_text, VOICE, rate="+2%")
        await communicate.save(out_path)

    asyncio.run(_generate())

    print(f"Saved voiceover to {out_path}")
    return out_path


if __name__ == "__main__":
    generate_voiceover()

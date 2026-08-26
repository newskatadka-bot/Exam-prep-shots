"""
Step 4 — Build the video as a sequence of clean text/equation slides
(question -> each solution step -> final answer), synced to the
voiceover, with burned-in captions. Uses Pillow to render slides and
ffmpeg (free, open source) to assemble the video.
"""
import os
import json
import subprocess
import textwrap
from PIL import Image, ImageDraw, ImageFont
from mutagen.mp3 import MP3

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")
SLIDES_DIR = os.path.join(OUTPUT_DIR, "slides")
W, H = 1080, 1920

BG_COLOR = (20, 24, 38)
ACCENT_COLOR = (90, 170, 255)
TEXT_COLOR = (245, 245, 250)
LABEL_COLOR = (140, 150, 175)


def get_font(size, bold=False):
    # DejaVuSans ships with Pillow's default font set on most systems
    try:
        path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold \
            else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def wrap_text(text, width_chars=28):
    return textwrap.wrap(text, width=width_chars)


def draw_centered_lines(draw, lines, font, y_start, line_height, color, max_width=920):
    y = y_start
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        w = bbox[2] - bbox[0]
        x = (W - w) // 2
        draw.text((x, y), line, font=font, fill=color)
        y += line_height
    return y


def make_slide(label, body_text, out_path, subject_tag=""):
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    label_font = get_font(46, bold=True)
    body_font = get_font(52)
    tag_font = get_font(34)

    if subject_tag:
        draw.text((60, 80), subject_tag, font=tag_font, fill=LABEL_COLOR)

    draw.rectangle([60, 160, 200, 172], fill=ACCENT_COLOR)
    draw.text((60, 190), label, font=label_font, fill=ACCENT_COLOR)

    lines = wrap_text(body_text, width_chars=24)
    total_h = len(lines) * 74
    y_start = max(400, (H - total_h) // 2)
    draw_centered_lines(draw, lines, body_font, y_start, 74, TEXT_COLOR)

    img.save(out_path)


def get_audio_duration(audio_path):
    return MP3(audio_path).info.length


def build_captions_srt(script_path, duration, out_path):
    with open(script_path) as f:
        text = f.read().strip()
    words = text.split()
    chunk_size = 5
    chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    per_chunk = duration / max(len(chunks), 1)

    def fmt(t):
        h, m, s = int(t // 3600), int((t % 3600) // 60), int(t % 60)
        ms = int((t - int(t)) * 1000)
        return f"{h:02}:{m:02}:{s:02},{ms:03}"

    with open(out_path, "w") as f:
        for i, chunk in enumerate(chunks):
            f.write(f"{i+1}\n{fmt(i*per_chunk)} --> {fmt((i+1)*per_chunk)}\n{chunk}\n\n")


def generate_video(out_path=None):
    audio_path = os.path.join(OUTPUT_DIR, "voiceover.mp3")
    script_path = os.path.join(OUTPUT_DIR, "script.txt")
    qa_path = os.path.join(OUTPUT_DIR, "qa_data.json")
    out_path = out_path or os.path.join(OUTPUT_DIR, "video.mp4")
    srt_path = os.path.join(OUTPUT_DIR, "captions.srt")

    os.makedirs(SLIDES_DIR, exist_ok=True)

    with open(qa_path) as f:
        qa = json.load(f)

    duration = get_audio_duration(audio_path)
    build_captions_srt(script_path, duration, srt_path)

    tag = f"{qa['board']} Class {qa['class']} - {qa['subject']}"

    slide_specs = [("QUESTION", qa["question"])]
    for i, step in enumerate(qa["steps"], 1):
        slide_specs.append((f"STEP {i}", step))
    slide_specs.append(("ANSWER", qa["answer"]))

    slide_paths = []
    for i, (label, body) in enumerate(slide_specs):
        p = os.path.join(SLIDES_DIR, f"slide_{i}.png")
        make_slide(label, body, p, subject_tag=tag)
        slide_paths.append(p)

    per_slide = duration / len(slide_paths)

    concat_path = os.path.join(OUTPUT_DIR, "slides_concat.txt")
    with open(concat_path, "w") as f:
        for p in slide_paths:
            f.write(f"file '{os.path.abspath(p)}'\nduration {per_slide:.2f}\n")
        f.write(f"file '{os.path.abspath(slide_paths[-1])}'\n")

    slideshow_path = os.path.join(OUTPUT_DIR, "slideshow.mp4")
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", concat_path,
        "-vsync", "vfr",
        "-pix_fmt", "yuv420p",
        slideshow_path,
    ], check=True)

    subprocess.run([
        "ffmpeg", "-y",
        "-i", slideshow_path,
        "-i", audio_path,
        "-vf", (
            f"subtitles={srt_path}:force_style='FontSize=28,PrimaryColour=&HFFFFFF&,"
            f"OutlineColour=&H000000&,BorderStyle=3,Outline=2,Alignment=2,MarginV=100,Bold=1'"
        ),
        "-c:v", "libx264", "-preset", "fast",
        "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-shortest",
        out_path,
    ], check=True)

    print(f"Saved video to {out_path}")
    return out_path


if __name__ == "__main__":
    generate_video()

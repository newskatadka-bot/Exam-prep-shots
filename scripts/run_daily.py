"""
Runs the entire daily pipeline: pick topic -> generate Q&A + script
-> voiceover -> slide video -> YouTube upload.
"""
import sys
import os

sys.path.append(os.path.dirname(__file__))
from importlib import import_module

write_script = import_module("2_write_script").write_script
generate_voice = import_module("3_generate_voice").generate_voiceover
generate_video = import_module("4_generate_video").generate_video
upload_youtube = import_module("5_upload_youtube").upload_short


def run_daily_pipeline():
    print("=== Step 1: Writing question + script ===")
    write_script()

    print("=== Step 2: Generating voiceover ===")
    generate_voice()

    print("=== Step 3: Generating video ===")
    generate_video()

    print("=== Step 4: Uploading to YouTube ===")
    upload_youtube()

    print("=== Done. Fully unattended run complete. ===")


if __name__ == "__main__":
    run_daily_pipeline()

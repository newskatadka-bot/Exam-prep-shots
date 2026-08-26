"""
Step 5 — Upload the finished video to YouTube as a public Short.
Requires one-time OAuth setup (youtube_token.json) — same as before.
"""
import os
import json
import pickle
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

load_dotenv()
TOKEN_FILE = os.getenv("YOUTUBE_TOKEN_FILE", "youtube_token.json")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")


def get_authenticated_service():
    with open(TOKEN_FILE, "rb") as f:
        creds = pickle.load(f)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return build("youtube", "v3", credentials=creds)


def upload_short(video_path=None):
    video_path = video_path or os.path.join(OUTPUT_DIR, "video.mp4")

    qa_path = os.path.join(OUTPUT_DIR, "qa_data.json")
    with open(qa_path) as f:
        qa = json.load(f)

    title = f"{qa['board']} Class {qa['class']} {qa['subject']} — {qa['chapter']} PYQ Solved #shorts"
    description = (
        f"{qa['board']} Class {qa['class']} {qa['subject']} — {qa['chapter']}\n\n"
        f"Q: {qa['question']}\n\nWatch for the full step-by-step solution!\n"
        "New question daily. #shorts #cbse #boardexam #physics #chemistry #maths"
    )

    youtube = get_authenticated_service()
    body = {
        "snippet": {
            "title": title[:100],
            "description": description,
            "tags": ["cbse", "board exam", qa["subject"], "pyq", "previous year questions", "shorts"],
            "categoryId": "27",  # Education
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False,
        },
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/mp4")
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Upload progress: {int(status.progress() * 100)}%")

    print(f"Uploaded: https://youtube.com/shorts/{response['id']}")
    return response["id"]


if __name__ == "__main__":
    upload_short()

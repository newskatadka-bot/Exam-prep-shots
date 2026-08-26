"""
Step 2 — Generate a board-exam-style question with a full step-by-step
solution and spoken explanation, for today's rotating topic. Uses
Google's Gemini API (free tier). Also saves structured Q&A data for
the slide-generation step.
"""
import os
import json
import sys

sys.path.append(os.path.dirname(__file__))
from topics_config import get_todays_topic

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """You are an expert Indian board exam tutor creating a
60-90 second YouTube Short. You will be given a board, class, subject,
and chapter. Write:

1. One realistic previous-year-exam-style question from that chapter
   (matching the actual difficulty and phrasing style of real board
   exam papers)
2. A clear step-by-step solution (3-5 concise steps)
3. The final answer

Then write a SPOKEN narration script explaining this in Hinglish
(natural Hindi-English mix, clear and encouraging, like a favorite
teacher explaining it simply) that:
- Reads the question clearly
- Walks through each step briefly and clearly (don't rush key formulas)
- States the final answer clearly
- Ends with one quick exam tip related to this topic

Keep the narration to ~140-170 words (60-75 seconds spoken).

Respond ONLY in this exact JSON format, no markdown, no extra text:
{
  "question": "the question text",
  "steps": ["step 1", "step 2", "step 3"],
  "answer": "final answer",
  "narration": "the full spoken script"
}"""


def write_script(out_dir=None):
    out_dir = out_dir or os.path.join(os.path.dirname(__file__), "..", "output")
    os.makedirs(out_dir, exist_ok=True)

    board, cls, subject, chapter = get_todays_topic()
    print(f"Today's topic: {board} Class {cls} {subject} - {chapter}")

    model = genai.GenerativeModel(
        model_name="gemini-3.6-flash",
        system_instruction=SYSTEM_PROMPT,
        generation_config={"temperature": 0.7, "response_mime_type": "application/json"},
    )
    response = model.generate_content(
        f"Board: {board}\nClass: {cls}\nSubject: {subject}\nChapter: {chapter}"
    )

    qa_data = json.loads(response.text)
    qa_data["board"] = board
    qa_data["class"] = cls
    qa_data["subject"] = subject
    qa_data["chapter"] = chapter

    qa_path = os.path.join(out_dir, "qa_data.json")
    with open(qa_path, "w") as f:
        json.dump(qa_data, f, indent=2, ensure_ascii=False)

    script_path = os.path.join(out_dir, "script.txt")
    with open(script_path, "w") as f:
        f.write(qa_data["narration"])

    print(f"Saved Q&A data to {qa_path}")
    print(f"Saved narration script to {script_path}")
    return qa_data


if __name__ == "__main__":
    write_script()

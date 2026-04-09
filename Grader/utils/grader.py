import json
import os
from google import genai
from dotenv import load_dotenv

from models.GraderResponse import GraderResponse

load_dotenv()

client = genai.Client(api_key=os.getenv("API_KEY"))

def grader(question, answer, max_score=1):
    prompt = f"""
You are a precise exam grader. Grade the student's answer, be fair and judgmental.

Return ONLY valid JSON with this exact schema:
{{
  "score": integer,
  "max_score": integer,
  "feedback": string,
  "missing_points": [string],
  "confidence": number
}}

Question:
{question}

Max Score: {max_score}

Student Answer:
\"\"\"
{answer}
\"\"\"

Rules:
Score must be between 0 and max_score based on correct answers
Feedback should be concise and clear
missing_points should list missed points on incorrect answers (e.g. missing_points = ["Point 2", "Point 3"]) - ["Point 2"] for question answer 2
confidence should be a float number between 0.0 and 1.0 based on judging confidence
Return JSON only
    
"""

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=genai.types.GenerateContentConfig(
            temperature=0,
            response_mime_type="application/json",
        )
    )

    content = response.text.strip()
    parsed_content = json.loads(content)

    return GraderResponse(**parsed_content)
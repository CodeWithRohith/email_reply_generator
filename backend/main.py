from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path
import os

# Load API key from .env
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load Gemini 1.5 Flash model
model = genai.GenerativeModel("gemini-1.5-flash")

app = FastAPI()

# Request body model
class EmailReplyRequest(BaseModel):
    email: str
    tone: str  # e.g., Formal, Friendly, Sarcastic

@app.post("/generate_reply")
def generate_reply(data: EmailReplyRequest):
    prompt = (
        f"You received the following email:\n\n"
        f"\"{data.email}\"\n\n"
        f"Write a {data.tone.lower()} reply to this email."
    )

    try:
        response = model.generate_content(prompt)
        return {"reply": response.text.strip()}
    except Exception as e:
        return {"error": str(e)}

class ImproveRequest(BaseModel):
    email: str

@app.post("/improve_email")
def improve_email(data: ImproveRequest):
    prompt = (
        f"Improve the following email to sound professional, clear, and polite:\n\n"
        f"{data.email}"
    )
    try:
        response = model.generate_content(prompt)
        return {"improved": response.text.strip()}
    except Exception as e:
        return {"error": str(e)}

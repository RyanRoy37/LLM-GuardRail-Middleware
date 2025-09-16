# endpoint.py (example)
from fastapi import FastAPI
from pydantic import BaseModel
import model
import filter
import db

class Prompt(BaseModel):
    prompt_id: str
    question: str
    description: str | None = None
    session_id: str


app = FastAPI()
@app.post("/prompt")
async def validate_prompt(prompt: Prompt):
    banned_word = filter.contains_banned_word(prompt.question)
    if banned_word is not None:
        db.logging(prompt.prompt_id,prompt.question, False, banned_word,prompt.session_id)
        return {f"Banned Word Detected.{banned_word} Please refrain from using this word."}
    prompt_question = filter.mask_sensitive_info(prompt.question)
    pred = model.predict(prompt_question)

    if pred == 1:
        db.logging(prompt.prompt_id,prompt.question, True, banned_word,prompt.session_id)
        return {"Unusual Prompt (Potential Jailbreak/Prompt injection attack) Detected. Please rephrase"}
    else:
        db.logging(prompt.prompt_id,prompt.question, False, banned_word, prompt.session_id)
        return {"Prompt is valid and safe to use."}

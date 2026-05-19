from fastapi import FastAPI, Depends, HTTPException, Header
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

llm = OpenAI()

@app.post("/talk")
def talk(prompt: str):
    response = llm.responses.create(
        model="gpt-5-mini-2025-08-07",
        input=prompt
    )

    return {
        "response": response.output_text
    }


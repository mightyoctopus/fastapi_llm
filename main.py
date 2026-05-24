from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from ai.gpt import Gpt
from auth.dependencies import get_user_identifier
from auth.throttling import apply_rate_limit

load_dotenv()
# Set credit remaining -- {api_key: credit_num}
API_KEY_CREDITS = {os.getenv("OPENAI_API_KEY"): 5}

app = FastAPI()



def load_system_prompt():
    try:
        with open("prompts/system_prompt.md") as f:
            return f.read()
    except FileNotFoundError:
        return None

system_prompt = load_system_prompt()



# Pydantic Models
class ChatRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    response: str


# API Endpoints
@app.post("/chat", response_model=ChatResponse)
def talk(request: ChatRequest, user_id: str = Depends(get_user_identifier)):
    apply_rate_limit(user_id)
    llm = Gpt(system_prompt)
    response = llm.chat(request.prompt)

    return {
        "response": response
    }


@app.get("/")
def root():
    return {"message": "API is running -- Homepage"}
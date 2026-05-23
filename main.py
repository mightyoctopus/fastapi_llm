from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from ai.gpt import Gpt

load_dotenv()
# Set credit remaining -- {api_key: credit_num}
API_KEY_CREDITS = {os.getenv("OPENAI_API_KEY"): 5}

app = FastAPI()




def verify_api_key(x_api_key: str = Header(None)):
    # If the api key matches the actual api key, then the credits var holds the value.
    # Otherwise, the api key is wrong, then it becomes 0 (This one also includes the error handling for wrong API key)
    credits = API_KEY_CREDITS.get(x_api_key, 0)
    print("CREDITS REMAINING: ", credits)

    if credits <= 0:
        raise HTTPException(status_code=401, detail="Invalid API Key or credits do not remain now.")
    return x_api_key


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
def talk(request: ChatRequest, x_api_key: str = Depends(verify_api_key)):

    print(f"USER PROMPT: {request.prompt}")
    API_KEY_CREDITS[x_api_key] -= 1

    llm = Gpt(x_api_key, system_prompt)
    response = llm.chat(request.prompt)

    return {
        "response": response
    }


@app.get("/")
def root():
    return {"message": "API is running -- Homepage"}
from fastapi import FastAPI, Depends, HTTPException, Header
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
# Set credit remaining -- {api_key: credit_num}
API_KEY_CREDITS = {os.getenv("OPENAI_API_KEY"): 5}

app = FastAPI()

llm = OpenAI()


def verify_api_key(x_api_key: str = Header(None)):
    credits = API_KEY_CREDITS.get(x_api_key, 0)
    print("CREDITS REMAINING: ", credits)

    if credits <= 0:
        raise HTTPException(status_code=401, detail="Invalid API Key or credits do not remain now.")
    return x_api_key


@app.post("/talk")
def talk(prompt: str, x_api_key: str = Depends(verify_api_key)):

    print(f"USER PROMPT: {prompt}")
    API_KEY_CREDITS[x_api_key] -= 1

    response = llm.responses.create(
        model="gpt-5-mini-2025-08-07",
        instructions="You are a helpful assistant",
        input=prompt
    )
    print(f"AI: {response.output_text}")

    return {
        "response": response.output_text
    }

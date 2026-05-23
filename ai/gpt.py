from openai import OpenAI
from .base import AIPlatform

class Gpt(AIPlatform):
    def __init__(self, api_key: str, system_prompt: str = None):
        self.api_key = api_key
        self.system_prompt = system_prompt
        self.llm = OpenAI(api_key=self.api_key)


    def chat(self, user_prompt: str) -> str:

        response = self.llm.responses.create(
            model="gpt-5-mini-2025-08-07",
            instructions=self.system_prompt,
            input=user_prompt
        )

        print(f"AI: {response.output_text}")

        return response.output_text




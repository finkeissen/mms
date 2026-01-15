from typing import Optional
from openai import OpenAI


class OpenAIProvider:
    def __init__(self, api_key: str, model: str, temperature: float):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.temperature = temperature

    def complete(self, prompt_text: str) -> str:
        r = self.client.responses.create(
            model=self.model,
            input=prompt_text,
            temperature=self.temperature
        )
        return r.output_text


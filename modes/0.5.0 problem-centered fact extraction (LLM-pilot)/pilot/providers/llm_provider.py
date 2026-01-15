from openai import OpenAI


class LMStudioProvider:
    """
    LM Studio exposes an OpenAI-compatible API endpoint.
    Default: http://localhost:1234/v1
    """

    def __init__(
        self,
        model: str,
        temperature: float,
        base_url: str = "http://localhost:1234/v1"
    ):
        self.client = OpenAI(
            api_key="lm-studio",
            base_url=base_url
        )
        self.model = model
        self.temperature = temperature

    def complete(self, prompt_text: str) -> str:
        r = self.client.responses.create(
            model=self.model,
            input=prompt_text,
            temperature=self.temperature
        )
        return r.output_text


import openai
from .base import LLMProvider

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key, model="gpt-4"):
        openai.api_key = api_key
        self.model = model
    
    def analyze(self, components):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a PCI-DSS security expert..."},
                {"role": "user", "content": f"Analyze this architecture diagram: {components}"}
            ]
        )
        return response 
import openai
from .base import LLMProvider
from src.utils.config import Config

class OpenAIProvider(LLMProvider):
    """OpenAI implementation of LLM provider"""
    
    def __init__(self):
        config = Config.get_provider_config('openai')
        super().__init__(**config)
        
        # Configure OpenAI
        openai.api_key = self.config['api_key']
        if self.config.get('base_url'):
            openai.api_base = self.config['base_url']
    
    def _generate_content(self, prompt: str) -> str:
        """Generate content using OpenAI"""
        try:
            messages = [
                {"role": "system", "content": "You are a PCI-DSS security expert analyzing architecture diagrams."},
                {"role": "user", "content": prompt}
            ]
            
            response = openai.ChatCompletion.create(
                model=self.config['model'],
                messages=messages,
                temperature=self.config['temperature']
            )
            
            if Config.DEBUG:
                print(f"\nDebug - OpenAI Response:\n{response.choices[0].message.content}")
            
            return response.choices[0].message.content
            
        except Exception as e:
            if Config.DEBUG:
                print(f"OpenAI generation error: {e}")
            raise 
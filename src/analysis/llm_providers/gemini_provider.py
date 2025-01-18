import google.generativeai as genai
from .base import LLMProvider
from src.utils.config import Config

class GeminiProvider(LLMProvider):
    """Gemini implementation of LLM provider"""
    
    def __init__(self):
        config = Config.get_provider_config('gemini')
        super().__init__(**config)
        
        # Configure Gemini
        genai.configure(api_key=self.config['api_key'])
        self.model = genai.GenerativeModel(self.config['model'])
        
        # Store temperature for generation
        self.temperature = self.config.get('temperature', 0.3)
    
    def _generate_content(self, prompt: str) -> str:
        """Generate content using Gemini"""
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=self.temperature
                )
            )
            
            if Config.DEBUG:
                print(f"\nDebug - Gemini Response:\n{response.text}")
            return response.text
            
        except Exception as e:
            if Config.DEBUG:
                print(f"Gemini generation error: {e}")
            raise 
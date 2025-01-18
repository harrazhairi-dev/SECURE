from src.utils.config import Config
from .llm_providers import GeminiProvider, OpenAIProvider

class SecurityAnalyzer:
    """Main analyzer class that coordinates LLM providers"""
    
    _providers = {
        'gemini': GeminiProvider,
        'openai': OpenAIProvider
    }
    
    def __init__(self, provider_type=None):
        """Initialize with specified provider or default"""
        provider_type = provider_type or Config.DEFAULT_PROVIDER
        
        if provider_type not in self._providers:
            raise ValueError(f"Unsupported provider: {provider_type}")
        
        provider_class = self._providers[provider_type]
        self.provider = provider_class()
    
    def analyze_security(self, components):
        """Analyze security using configured provider"""
        try:
            if Config.DEBUG:
                print(f"Using provider: {self.provider.__class__.__name__}")
            
            return self.provider.analyze(components)
            
        except Exception as e:
            if Config.DEBUG:
                print(f"Analysis error: {e}")
            return self.provider._get_error_response()
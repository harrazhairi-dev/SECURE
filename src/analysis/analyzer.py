import os
from .llm_providers import GeminiProvider, OpenAIProvider

class SecurityAnalyzer:
    def __init__(self, provider_type="gemini"):
        if provider_type == "gemini":
            self.provider = GeminiProvider(os.getenv('GOOGLE_API_KEY'))
        elif provider_type == "openai":
            self.provider = OpenAIProvider(os.getenv('OPENAI_API_KEY'))
        else:
            raise ValueError(f"Unsupported provider: {provider_type}")

    def analyze_security(self, components):
        try:
            results = self.provider.analyze(components)
            # Process results...
            return results
        except Exception as e:
            print(f"Error during analysis: {e}")
            return self._get_error_response()

    def _get_error_response(self):
        # Your existing error response structure
        return {
            "checks": {...},
            "recommendations": [...],
            "analysis": {...}
        }
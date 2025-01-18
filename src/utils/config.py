import os
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables
load_dotenv()

class Config:
    """Unified configuration for the Architecture Security Checker"""
    
    # Debug Settings
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Determine default provider based on available API keys
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Default to Gemini if available, otherwise warn during validation
    DEFAULT_PROVIDER = os.getenv('DEFAULT_PROVIDER', 'gemini')
    
    # Provider Configurations
    PROVIDERS: Dict[str, Dict[str, Any]] = {
        'gemini': {
            'api_key': GOOGLE_API_KEY,
            'model': 'gemini-pro',
            'temperature': 0.3,
        },
        'openai': {
            'api_key': OPENAI_API_KEY,
            'base_url': os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1'),
            'model': os.getenv('OPENAI_MODEL', 'gpt-4'),
            'temperature': 0.3,
        }
    }
    
    # Response Format Schema (used by all providers)
    RESPONSE_SCHEMA = {
        "checks": {
            "Firewalls present": "bool",
            "Network segmentation": "bool",
            "CDE isolation": "bool",
            "Encryption in transit": "bool",
            "Encryption at rest": "bool",
            "Access controls": "bool",
            "Audit logging": "bool"
        },
        "compliance_score": "string",
        "recommendations": ["string"],
        "analysis": {
            "architecture_patterns": ["string"],
            "security_zones": ["string"],
            "key_risks": ["string"],
            "attack_vectors": ["string"],
            "security_controls": ["string"]
        },
        "note": "string"
    }
    
    @classmethod
    def get_provider_config(cls, provider_name: str) -> Dict[str, Any]:
        """Get configuration for specific provider"""
        if provider_name not in cls.PROVIDERS:
            raise ValueError(f"Unsupported provider: {provider_name}")
            
        config = cls.PROVIDERS[provider_name]
        if not config.get('api_key'):
            if provider_name == cls.DEFAULT_PROVIDER:
                raise ValueError(f"API key not found for default provider: {provider_name}")
            elif cls.DEBUG:
                print(f"Warning: API key not found for provider: {provider_name}")
        return config
    
    @classmethod
    def validate(cls):
        """Validate configuration"""
        # Ensure at least one provider is configured
        if not cls.GOOGLE_API_KEY and not cls.OPENAI_API_KEY:
            raise ValueError("No API keys found. Please configure at least one provider (Gemini or OpenAI)")
        
        # If default provider is OpenAI but no key, switch to Gemini
        if cls.DEFAULT_PROVIDER == 'openai' and not cls.OPENAI_API_KEY:
            if cls.GOOGLE_API_KEY:
                if cls.DEBUG:
                    print("Warning: OpenAI key not found, falling back to Gemini")
                cls.DEFAULT_PROVIDER = 'gemini'
            else:
                raise ValueError("No available API keys found") 
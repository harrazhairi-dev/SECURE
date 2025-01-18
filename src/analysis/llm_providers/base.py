from abc import ABC, abstractmethod
from typing import Dict, Any
from src.utils.config import Config
import json

class LLMProvider(ABC):
    """Base class for LLM providers with standardized response handling"""
    
    def __init__(self, **kwargs):
        self.config = kwargs
    
    @abstractmethod
    def _generate_content(self, prompt: str) -> str:
        """Provider-specific method to generate content"""
        pass
    
    def analyze(self, components: Dict[str, Any]) -> Dict[str, Any]:
        """Standardized analysis method used by all providers"""
        try:
            # Generate the prompt using components
            prompt = self._create_prompt(components)
            
            # Get raw response from provider
            raw_response = self._generate_content(prompt)
            
            # Parse and validate response
            results = self._parse_response(raw_response)
            
            # Add standard note
            results["note"] = "This is an automated initial assessment. Please consult security team for detailed review."
            
            return results
            
        except Exception as e:
            if Config.DEBUG:
                print(f"Error in {self.__class__.__name__}: {e}")
            return self._get_error_response()
    
    def _create_prompt(self, components: Dict[str, Any]) -> str:
        """Create standardized prompt for all providers"""
        return f"""
        You are a PCI-DSS security expert analyzing an architecture diagram for security compliance.

        **Detected Components:**
        {json.dumps(components['detected_items'], indent=2)}

        **Raw Text:**
        {components['text']}

        **Instructions:**
        1. **Evaluate PCI-DSS Compliance:**
           - Are firewalls present and properly configured to protect cardholder data?
           - Are vendor-supplied defaults (e.g., passwords, configurations) replaced with secure settings?
           - Is cardholder data encrypted at rest and in transit?
           - Are access controls in place to restrict access to cardholder data?
           - Are audit logs enabled for all critical systems?

        2. **Analyze Security Patterns:**
           - Are client-facing components (e.g., web servers) properly isolated from internal systems?
           - Are network boundaries (e.g., DMZ, private zones) clearly defined and enforced?
           - Are security controls (e.g., firewalls, IDS/IPS, WAF) in place to protect critical assets?

        3. **Identify Risks and Gaps:**
           - Identify potential attack vectors (e.g., exposed databases, unencrypted communication).
           - Highlight security gaps (e.g., missing segmentation, lack of encryption).
           - Suggest specific controls to mitigate risks (e.g., WAF for web servers, encryption for databases).

        4. **Provide Recommendations:**
           - Offer clear, actionable recommendations to address identified issues.
           - Prioritize recommendations based on risk severity (e.g., critical, high, medium).

        5. **Assign a Compliance Score:**
           - Provide a compliance score (High/Medium/Low) based on the analysis.
           - Explain the rationale for the score.

        Respond ONLY with a valid JSON object matching exactly this schema:
        {json.dumps(Config.RESPONSE_SCHEMA, indent=2)}
        """
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse and validate provider response"""
        clean_response = response.strip()
        if clean_response.startswith('```json'):
            clean_response = clean_response[7:-3]
        
        return json.loads(clean_response)
    
    def _get_error_response(self) -> Dict[str, Any]:
        """Standard error response for all providers"""
        return {
            "checks": {
                "Firewalls present": False,
                "Network segmentation": False,
                "CDE isolation": False,
                "Encryption in transit": False,
                "Encryption at rest": False,
                "Access controls": False,
                "Audit logging": False
            },
            "compliance_score": "Low",
            "recommendations": [
                "Analysis failed - please check the diagram clarity",
                "Ensure all security components are clearly labeled"
            ],
            "analysis": {
                "architecture_patterns": [],
                "security_zones": [],
                "key_risks": ["Analysis incomplete due to error"],
                "attack_vectors": [],
                "security_controls": []
            },
            "note": "This is an automated initial assessment. Please consult security team for detailed review."
        } 
#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}Setting up Architecture Security Checker...${NC}"

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if (( $(echo "$python_version < 3.8" | bc -l) )); then
    echo -e "${RED}Error: Python 3.8 or higher is required${NC}"
    exit 1
fi

# Check for Tesseract OCR
if ! command -v tesseract &> /dev/null; then
    echo -e "${RED}Error: Tesseract OCR is not installed${NC}"
    echo "Please install Tesseract OCR:"
    echo "  MacOS:     brew install tesseract"
    echo "  Ubuntu:    sudo apt-get install tesseract-ocr"
    echo "  Windows:   https://github.com/UB-Mannheim/tesseract/wiki"
    exit 1
fi

# Create directory structure
mkdir -p src/{ocr,analysis/llm_providers,utils}
mkdir -p tests/test_diagrams

# Create virtual environment
echo -e "${BLUE}Creating virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Create requirements.txt
cat > requirements.txt << 'EOL'
# Core dependencies
python-dotenv>=1.0.0
Pillow>=10.0.0
pytesseract>=0.3.10
opencv-python>=4.8.0

# LLM Provider dependencies
google-generativeai>=0.3.0
openai>=1.0.0  # Optional, for OpenAI support
EOL

# Create .env template
cat > .env.template << 'EOL'
# Debug Mode
DEBUG=True

# Default Provider (gemini or openai)
DEFAULT_PROVIDER=gemini

# Gemini Settings
GOOGLE_API_KEY=your-gemini-api-key

# OpenAI Settings (optional)
#OPENAI_API_KEY=your-openai-api-key
#OPENAI_BASE_URL=https://api.openai.com/v1
#OPENAI_MODEL=gpt-4
EOL

# Create package initializers
echo "Creating package initializers..."
touch src/__init__.py
touch src/ocr/__init__.py
touch src/analysis/__init__.py
touch src/utils/__init__.py

cat > src/analysis/llm_providers/__init__.py << 'EOL'
from .gemini_provider import GeminiProvider
from .openai_provider import OpenAIProvider

__all__ = ['GeminiProvider', 'OpenAIProvider']
EOL

# Create main.py
cat > main.py << 'EOL'
import argparse
from src.ocr.extractor import extract_components
from src.analysis.analyzer import SecurityAnalyzer

def main():
    parser = argparse.ArgumentParser(description="Analyze architecture diagrams for security compliance")
    parser.add_argument("image_path", help="Path to the architecture diagram image")
    parser.add_argument("--provider", default="gemini", choices=["gemini", "openai"], help="LLM provider to use")
    args = parser.parse_args()

    # Extract components using OCR
    print(f"Analyzing diagram: {args.image_path}")
    components = extract_components(args.image_path)
    
    # Initialize analyzer with specified provider
    analyzer = SecurityAnalyzer(provider_type=args.provider)
    results = analyzer.analyze_security(components)
    
    # Print results
    print("\nQuick Security Check Results:")
    for check, status in results["checks"].items():
        symbol = "✓" if status else "✗"
        print(f"{symbol} {check}")
    
    print("\nArchitecture Patterns:")
    for pattern in results["analysis"]["architecture_patterns"]:
        print(f"- {pattern}")
        
    print("\nSecurity Zones:")
    for zone in results["analysis"]["security_zones"]:
        print(f"- {zone}")
        
    print("\nKey Security Risks:")
    for risk in results["analysis"]["key_risks"]:
        print(f"- {risk}")
    
    print("\nRecommendations:")
    for i, rec in enumerate(results["recommendations"], 1):
        print(f"{i}. {rec}")
        
    if "note" in results:
        print(f"\nNote: {results['note']}")

if __name__ == "__main__":
    main()
EOL

# Create OCR extractor
cat > src/ocr/extractor.py << 'EOL'
import pytesseract
from PIL import Image
import cv2
import numpy as np

def extract_components(image_path):
    """Extract components from architecture diagram using OCR."""
    try:
        # Read image
        image = cv2.imread(image_path)
        height, width = image.shape[:2]
        
        # Enlarge image
        scale_factor = 2
        image = cv2.resize(image, (width * scale_factor, height * scale_factor))
        
        # Convert to HSV to handle colored text better
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Create masks for different colored text
        # Dark text
        lower_black = np.array([0, 0, 0])
        upper_black = np.array([180, 255, 100])
        mask_black = cv2.inRange(hsv, lower_black, upper_black)
        
        # Process each color channel separately
        results = []
        
        # Process original and black mask
        for mask in [None, mask_black]:
            if mask is not None:
                processed = cv2.bitwise_and(image, image, mask=mask)
            else:
                processed = image.copy()
            
            # Convert to grayscale
            gray = cv2.cvtColor(processed, cv2.COLOR_BGR2GRAY)
            
            # Threshold
            _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # OCR with different PSM modes
            for psm in [3, 6, 11]:  # Try different page segmentation modes
                config = f'--oem 3 --psm {psm}'
                text = pytesseract.image_to_string(binary, config=config)
                results.extend([line.strip() for line in text.split('\n') if line.strip()])
        
        # Remove duplicates and empty lines
        unique_results = list(set(results))
        
        # Categorize detected components
        components = {
            "text": "\n".join(unique_results),
            "detected_items": {
                "client": [],
                "server": [],
                "data": [],
                "network": [],
                "interfaces": [],
                "security": []
            }
        }
        
        # Keywords to look for
        keywords = {
            "client": ["client", "web interface"],
            "server": ["server", "kernel", "system manager"],
            "data": ["sql", "database", "firebird", "data"],
            "network": ["internet", "intranet"],
            "interfaces": ["interface", "api", "access interface"],
            "security": ["firewall", "security", "rule"]
        }
        
        # Categorize each detected text
        for text in unique_results:
            text_lower = text.lower()
            for category, terms in keywords.items():
                if any(term in text_lower for term in terms):
                    components["detected_items"][category].append(text)
        
        print("\nDebug - Raw OCR Text:")
        print("\n".join(unique_results))
        
        print("\nDebug - Detected Components:")
        for category, items in components["detected_items"].items():
            if items:
                print(f"{category}: {items}")
        
        return components
        
    except Exception as e:
        print(f"Error in OCR processing: {e}")
        return {
            "text": "",
            "detected_items": {},
            "error": str(e)
        }
EOL

# Create LLM provider base class
cat > src/analysis/llm_providers/base.py << 'EOL'
from abc import ABC, abstractmethod

class LLMProvider(ABC):
    @abstractmethod
    def analyze(self, components):
        """Analyze components and return security assessment"""
        pass
EOL

# Create Gemini provider
cat > src/analysis/llm_providers/gemini_provider.py << 'EOL'
import google.generativeai as genai
from .base import LLMProvider
import json

class GeminiProvider(LLMProvider):
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def analyze(self, components):
        prompt = f"""
        You are a PCI-DSS security expert analyzing an architecture diagram.
        
        Diagram components detected: {components['detected_items']}
        Raw text found: {components['text']}

        Even if the text detection is imperfect, analyze the general architecture for basic security patterns.
        Focus on these key aspects:

        1. Basic Security Patterns:
           - Client/Internet facing components
           - Internal systems and databases
           - Network boundaries
        
        2. Common Security Issues:
           - Direct database exposure
           - Missing network segmentation
           - Lack of security controls
        
        3. PCI-DSS Basics:
           - Public/private separation
           - Data protection measures
           - Access control patterns

        Respond ONLY with a valid JSON object in this exact format:
        {{
            "checks": {{
                "Firewalls present": false,
                "Network segmentation": true,
                "CDE isolation": false
            }},
            "recommendations": [
                "Clear, actionable recommendation",
                "Focus on obvious security improvements"
            ],
            "analysis": {{
                "architecture_patterns": ["detected patterns"],
                "security_zones": ["identified boundaries"],
                "key_risks": ["main security concerns"]
            }}
        }}
        
        Be practical and focus on obvious security improvements.
        """
        
        response = self.model.generate_content(prompt)
        print("\nDebug - LLM Response:")
        print(response.text)
        
        # Clean and parse response
        clean_response = response.text.strip()
        if clean_response.startswith('```json'):
            clean_response = clean_response[7:-3]
        
        results = json.loads(clean_response)
        results["note"] = "This is an automated initial assessment. Please consult security team for detailed review."
        
        return results
EOL

# Create OpenAI provider
cat > src/analysis/llm_providers/openai_provider.py << 'EOL'
import openai
from .base import LLMProvider
import json
import os

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key, base_url=None, model="gpt-4"):
        openai.api_key = api_key
        if base_url:
            openai.api_base = base_url
        self.model = model
    
    def analyze(self, components):
        messages = [
            {
                "role": "system",
                "content": "You are a PCI-DSS security expert analyzing architecture diagrams."
            },
            {
                "role": "user",
                "content": f"""
                Analyze this architecture diagram for security compliance:
                Components detected: {components['detected_items']}
                Raw text: {components['text']}
                
                Focus on:
                1. Basic Security Patterns
                2. Common Security Issues
                3. PCI-DSS Basics
                
                Respond ONLY with a valid JSON object.
                """
            }
        ]
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages
        )
        
        results = json.loads(response.choices[0].message.content)
        results["note"] = "This is an automated initial assessment. Please consult security team for detailed review."
        
        return results
EOL

# Create security analyzer
cat > src/analysis/analyzer.py << 'EOL'
import os
from .llm_providers import GeminiProvider, OpenAIProvider

class SecurityAnalyzer:
    def __init__(self, provider_type="gemini"):
        if provider_type == "gemini":
            self.provider = GeminiProvider(os.getenv('GOOGLE_API_KEY'))
        elif provider_type == "openai":
            self.provider = OpenAIProvider(
                api_key=os.getenv('OPENAI_API_KEY'),
                base_url=os.getenv('OPENAI_BASE_URL')
            )
        else:
            raise ValueError(f"Unsupported provider: {provider_type}")

    def analyze_security(self, components):
        try:
            results = self.provider.analyze(components)
            return results
        except Exception as e:
            print(f"Error during analysis: {e}")
            return {
                "checks": {
                    "Firewalls present": False,
                    "Network segmentation": False,
                    "CDE isolation": False
                },
                "recommendations": [
                    "Unable to fully analyze diagram - please ensure it shows system boundaries and components clearly",
                    "Consider including network security controls in the diagram"
                ],
                "analysis": {
                    "architecture_patterns": [],
                    "security_zones": [],
                    "key_risks": ["Analysis incomplete - see recommendations"]
                },
                "note": "This is an automated initial assessment. Please consult security team for detailed review."
            }
EOL

# Create .gitignore
cat > .gitignore << 'EOL'
# Python
__pycache__/
*.py[cod]
*$py.class
venv/

# Environment
.env
.env.*
!.env.template

# IDE
.vscode/
.idea/

# Temp files
temp_*.png
*.log

# Test coverage
.coverage
htmlcov/
EOL

# Create README.md
cat > README.md << 'EOL'
# Architecture Security Checker

A tool to analyze architecture diagrams for PCI-DSS compliance.

## Setup
1. Create virtual environment and install dependencies:
```bash
./setup.sh
```

2. Copy .env.template to .env and configure your API keys:
```bash
cp .env.template .env
```

3. Run the analyzer:
```bash
python main.py path/to/diagram.png
```

## Configuration
- GOOGLE_API_KEY: Your Gemini API key
- OPENAI_API_KEY: Your OpenAI API key (if using OpenAI)
- OPENAI_BASE_URL: Custom OpenAI endpoint (optional)

## Usage
```bash
# Using Gemini (default)
python main.py diagram.png

# Using OpenAI
python main.py diagram.png --provider openai
```
EOL

# Make script executable
chmod +x setup.sh

# Install dependencies
echo -e "${BLUE}Installing dependencies...${NC}"
pip install -r requirements.txt

echo -e "${GREEN}Setup complete! Next steps:${NC}"
echo "1. Copy .env.template to .env:"
echo "   cp .env.template .env"
echo "2. Add your API key to .env"
echo "3. Run the analyzer:"
echo "   python main.py path/to/diagram.png"

# Optional: Create test diagram directory
mkdir -p tests/test_diagrams
echo -e "${BLUE}Created test_diagrams directory for your architecture diagrams${NC}" 
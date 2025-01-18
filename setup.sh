#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Setting up Architecture Security Checker...${NC}"

# Create directory structure
mkdir -p src/{ocr,analysis/llm_providers,utils}
mkdir -p tests/test_diagrams

# Create virtual environment
echo -e "${BLUE}Creating virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Create files with content
echo -e "${BLUE}Creating project files...${NC}"

# Create requirements files
cat > requirements.txt << 'EOL'
Pillow>=9.5.0
pytesseract>=0.3.10
google-cloud-vision>=3.4.4
google-generativeai>=0.3.2
python-dotenv>=1.0.0
opencv-python>=4.8.0
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

# Create source files
cat > src/ocr/extractor.py << 'EOL'
# [Previous extractor.py content]
EOL

cat > src/analysis/llm_providers/base.py << 'EOL'
# [Previous base.py content]
EOL

cat > src/analysis/llm_providers/gemini_provider.py << 'EOL'
# [Previous gemini_provider.py content]
EOL

cat > src/analysis/llm_providers/openai_provider.py << 'EOL'
# [Previous openai_provider.py content]
EOL

cat > src/analysis/analyzer.py << 'EOL'
# [Previous analyzer.py content]
EOL

# Create .env template
cat > .env.template << 'EOL'
# LLM Provider API Keys
GOOGLE_API_KEY=your-gemini-api-key
OPENAI_API_KEY=your-openai-api-key
OPENAI_BASE_URL=your-custom-openai-url

# Other Configuration
DEBUG=False
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
echo "1. Copy .env.template to .env and add your API keys"
echo "2. Run: python main.py path/to/diagram.png" 
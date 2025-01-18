import os
from pathlib import Path

# Project structure
DIRECTORIES = [
    "src",
    "src/ocr",
    "src/analysis",
    "src/utils",
    "tests",
]

# Initial files content
MAIN_PY = '''
import argparse
from src.ocr.extractor import extract_components
from src.analysis.analyzer import analyze_security

def main():
    parser = argparse.ArgumentParser(description="Analyze architecture diagrams for security compliance")
    parser.add_argument("image_path", help="Path to the architecture diagram image")
    args = parser.parse_args()

    # Extract components using OCR
    components = extract_components(args.image_path)
    
    # Analyze security
    results = analyze_security(components)
    
    # Print results
    print("\nQuick Security Check Results:")
    for check, status in results["checks"].items():
        symbol = "✓" if status else "✗"
        print(f"{symbol} {check}")
    
    print("\nRecommendations:")
    for i, rec in enumerate(results["recommendations"], 1):
        print(f"{i}. {rec}")

if __name__ == "__main__":
    main()
'''

EXTRACTOR_PY = '''
import pytesseract
from PIL import Image
from google.cloud import vision

def extract_components(image_path):
    """Extract components from architecture diagram using OCR."""
    # Basic implementation using Tesseract
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    
    # TODO: Implement more sophisticated extraction
    return {
        "text": text,
        "components": [],  # Will be populated with detected components
    }
'''

ANALYZER_PY = '''
import google.generativeai as genai
import os

# Configure Gemini
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def analyze_security(components):
    """Analyze extracted components for security compliance."""
    model = genai.GenerativeModel('gemini-pro')
    
    # Construct prompt
    prompt = f"""
    Analyze these architecture diagram components for basic PCI-DSS compliance:
    {components}
    
    Focus on:
    1. Firewall presence and placement
    2. Network segmentation (public vs private)
    3. CDE isolation
    
    Format the response as JSON with two keys:
    - checks: dict of compliance checks and their status
    - recommendations: list of specific improvements needed
    """
    
    try:
        response = model.generate_content(prompt)
        # TODO: Parse response and return structured results
        return {
            "checks": {
                "Firewalls present": True,
                "Network segmentation": False,
                "CDE isolation": False
            },
            "recommendations": [
                "Add clear network boundaries",
                "Implement proper CDE isolation"
            ]
        }
    except Exception as e:
        print(f"Error during analysis: {e}")
        return None
'''

README_MD = '''
# Architecture Security Checker

A tool to analyze architecture diagrams for PCI-DSS compliance.

## Setup
1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```
   export GOOGLE_API_KEY='your-gemini-api-key'
   ```

3. Run the analyzer:
   ```
   python main.py path/to/diagram.png
   ```
'''

def setup_project():
    # Create directories
    for dir_path in DIRECTORIES:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        Path(f"{dir_path}/__init__.py").touch()

    # Create files
    files = {
        "main.py": MAIN_PY,
        "src/ocr/extractor.py": EXTRACTOR_PY,
        "src/analysis/analyzer.py": ANALYZER_PY,
        "README.md": README_MD
    }

    for file_path, content in files.items():
        with open(file_path, "w") as f:
            f.write(content.strip())

    print("Project setup complete! Don't forget to:")
    print("1. Install Tesseract OCR on your system if not already installed")
    print("2. Set your GOOGLE_API_KEY environment variable")
    print("3. Create a test diagram to verify the setup")

if __name__ == "__main__":
    setup_project()
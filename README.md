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
# Architecture Security Checker

A comprehensive tool for analyzing architecture diagrams against PCI-DSS compliance requirements using OCR and LLM technology.

## Features

- **Automated Security Analysis**
  - PCI-DSS compliance checks
  - Network segmentation analysis
  - Security control detection
  - Risk identification

- **Multiple LLM Support**
  - Google Gemini (default)
  - OpenAI (optional)
  - Extensible for custom LLMs

- **Comprehensive Output**
  - Security checks status
  - Compliance scoring
  - Actionable recommendations
  - Attack vector analysis
  - Security control suggestions

## Prerequisites

1. Python 3.8 or higher
2. Tesseract OCR:
   ```bash
   # MacOS
   brew install tesseract
   
   # Ubuntu/Debian
   sudo apt-get install tesseract-ocr
   
   # Windows
   # Download from: https://github.com/UB-Mannheim/tesseract/wiki
   ```

## Quick Start

1. **Setup**
   ```bash
   git clone <repository-url>
   cd architecture-security-checker
   chmod +x setup.sh
   ./setup.sh
   ```

2. **Configuration**
   ```bash
   cp .env.template .env
   # Edit .env with your API keys
   ```

3. **Run Analysis**
   ```bash
   python main.py path/to/diagram.png
   ```

## Configuration Options

```plaintext
# .env file
DEBUG=True                    # Enable debug output
DEFAULT_PROVIDER=gemini       # Default LLM provider
GOOGLE_API_KEY=xxx           # Required for Gemini
OPENAI_API_KEY=xxx           # Optional, for OpenAI
OPENAI_BASE_URL=xxx          # Optional, for custom endpoints
OPENAI_MODEL=xxx             # Optional, default: gpt-4
```

## Analysis Output

1. **Security Checks**
   - Firewalls presence
   - Network segmentation
   - CDE isolation
   - Encryption (transit/rest)
   - Access controls
   - Audit logging

2. **Compliance Score**
   - High/Medium/Low rating
   - Scoring rationale

3. **Detailed Analysis**
   - Architecture patterns
   - Security zones
   - Key risks
   - Attack vectors
   - Security controls

4. **Recommendations**
   - Prioritized by severity
   - Actionable items
   - PCI-DSS specific guidance

## Best Practices

1. **Diagram Preparation**
   - Use high contrast
   - Label components clearly
   - Show network boundaries
   - Include security controls

2. **Analysis Review**
   - Verify automated findings
   - Consult security team
   - Document decisions

## Troubleshooting

1. **OCR Issues**
   - Ensure clear text
   - Check image quality
   - Verify Tesseract installation

2. **LLM Issues**
   - Verify API keys
   - Check network connectivity
   - Enable DEBUG mode

## Project Structure
```
architecture-security-checker/
├── src/
│   ├── ocr/                  # OCR processing
│   ├── analysis/            # Security analysis
│   │   ├── llm_providers/   # LLM integrations
│   │   └── analyzer.py
│   └── utils/              # Shared utilities
├── tests/
├── main.py                 # Entry point
├── setup.sh               # Setup script
└── README.md
```

## Limitations

- Focused on PCI-DSS requirements
- OCR quality dependent
- Static analysis only
- No persistent storage

## Support

- GitHub Issues
- Documentation
- Example diagrams

## License

[Your License Here]
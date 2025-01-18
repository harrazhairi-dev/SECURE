# Architecture Security Checker

A tool that analyzes architecture diagrams for PCI-DSS compliance using OCR and LLM technology. It can detect basic security patterns, network segmentation, and provide recommendations.

## Prerequisites

1. Python 3.8 or higher
2. Tesseract OCR installed:
   ```bash
   # For MacOS
   brew install tesseract
   
   # For Ubuntu/Debian
   sudo apt-get install tesseract-ocr
   
   # For Windows
   # Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
   ```

## Initial Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/harrazhairi-dev/SECURE.git
   cd SECURE
   ```

2. Run the setup script:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. Create and configure your environment file:
   ```bash
   cp .env.template .env
   ```

4. Edit `.env` with your API keys:
   ```plaintext
   # For Gemini (Default)
   GOOGLE_API_KEY=your-gemini-api-key
   
   # For OpenAI or Custom LLM
   OPENAI_API_KEY=your-openai-api-key
   OPENAI_BASE_URL=your-custom-endpoint  # Optional, for private LLMs
   ```

## Usage

### Basic Usage (Gemini)
```bash
# Activate virtual environment (if not already activated)
source venv/bin/activate  # On Unix/MacOS
# or
.\venv\Scripts\activate  # On Windows

# Run analysis on a diagram
python main.py path/to/your/diagram.png
```

### Using OpenAI or Custom LLM
```bash
python main.py path/to/your/diagram.png --provider openai
```

## Understanding the Output

The tool provides several sections of analysis:

1. **Quick Security Check Results**
   ```
   ✓ Firewalls present
   ✗ Network segmentation
   ✗ CDE isolation
   ```

2. **Architecture Patterns**
   - Identifies architectural styles
   - Lists major components

3. **Security Zones**
   - Identifies network boundaries
   - Lists security domains

4. **Key Security Risks**
   - Highlights potential vulnerabilities
   - Identifies missing controls

5. **Recommendations**
   - Actionable improvements
   - PCI-DSS specific suggestions

## Supported Diagram Types

- PNG and JPG formats
- Architecture diagrams showing:
  - Network components
  - System boundaries
  - Data flows
  - Security controls

## Troubleshooting

### OCR Issues
If the tool isn't detecting text correctly:
1. Ensure diagram text is clear and readable
2. Try increasing image resolution
3. Ensure good contrast between text and background

### API Key Issues
If you get authentication errors:
1. Check your `.env` file has correct API keys
2. Ensure keys have necessary permissions
3. For custom LLMs, verify the BASE_URL is correct

### General Issues
1. Check virtual environment is activated
2. Verify all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure Tesseract OCR is properly installed:
   ```bash
   tesseract --version
   ```

## Project Structure
```
arch-security-checker/
├── src/
│   ├── ocr/
│   │   └── extractor.py          # OCR processing
│   ├── analysis/
│   │   ├── llm_providers/        # LLM integrations
│   │   │   ├── base.py
│   │   │   ├── gemini_provider.py
│   │   │   └── openai_provider.py
│   │   └── analyzer.py           # Main analysis logic
│   └── utils/
├── tests/
│   └── test_diagrams/           # Test images
├── requirements.txt             # Dependencies
├── .env.template               # Environment template
├── setup.sh                    # Setup script
└── main.py                     # Entry point
```

## Using with Private LLMs

1. Configure your private LLM endpoint:
   ```plaintext
   # .env file
   OPENAI_API_KEY=your-private-key
   OPENAI_BASE_URL=https://your-llm-endpoint.com/v1
   ```

2. Run with OpenAI provider:
   ```bash
   python main.py diagram.png --provider openai
   ```

## Best Practices

1. **Diagram Preparation**
   - Use high contrast colors
   - Include clear component labels
   - Show network boundaries
   - Mark security controls

2. **Security Analysis**
   - Review all recommendations
   - Validate findings manually
   - Consult security team for critical systems

3. **Regular Updates**
   - Keep dependencies updated
   - Update API keys as needed
   - Check for tool updates

## Limitations

- Basic PCI-DSS checks only
- OCR accuracy depends on diagram quality
- No persistent storage of results
- Limited to static diagram analysis

## Support

For issues and feature requests:
1. Check troubleshooting guide above
2. Open an issue on GitHub
3. Include sample diagram (if possible)

## License

[Your License Here]
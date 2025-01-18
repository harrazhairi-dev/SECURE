import argparse
from src.ocr.extractor import extract_components
from src.analysis.analyzer import SecurityAnalyzer
from src.utils.config import Config

def main():
    # Validate configuration
    Config.validate()
    
    parser = argparse.ArgumentParser(description="Analyze architecture diagrams for security compliance")
    parser.add_argument("image_path", help="Path to the architecture diagram image")
    parser.add_argument("--provider", default=Config.DEFAULT_PROVIDER, 
                       choices=["gemini", "openai"], help="LLM provider to use")
    args = parser.parse_args()

    # Extract components using OCR
    print(f"Analyzing diagram: {args.image_path}")
    components = extract_components(args.image_path)
    
    # Analyze security
    analyzer = SecurityAnalyzer(provider_type=args.provider)
    results = analyzer.analyze_security(components)
    
    # Print results
    print("\nSecurity Check Results:")
    for check, status in results["checks"].items():
        symbol = "✓" if status else "✗"
        print(f"{symbol} {check}")
    
    print(f"\nCompliance Score: {results['compliance_score']}")
    
    print("\nRecommendations:")
    for i, rec in enumerate(results["recommendations"], 1):
        print(f"{i}. {rec}")
    
    print("\nAnalysis Details:")
    for category, items in results["analysis"].items():
        if items:  # Only print non-empty categories
            print(f"\n{category.replace('_', ' ').title()}:")
            for item in items:
                print(f"- {item}")
    
    if "note" in results:
        print(f"\nNote: {results['note']}")

if __name__ == "__main__":
    main()
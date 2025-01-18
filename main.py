import argparse
from src.ocr.extractor import extract_components
from src.analysis.analyzer import analyze_security

def main():
    parser = argparse.ArgumentParser(description="Analyze architecture diagrams for security compliance")
    parser.add_argument("image_path", help="Path to the architecture diagram image")
    args = parser.parse_args()

    # Extract components using OCR
    print(f"Analyzing diagram: {args.image_path}")
    components = extract_components(args.image_path)
    
    # Analyze security
    results = analyze_security(components)
    
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
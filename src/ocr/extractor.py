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
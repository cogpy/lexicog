#!/usr/bin/env python3
"""
Extract all AD paragraph numbers from the founding affidavit to create
a complete 144-paragraph reference file.
"""
import re
from pathlib import Path

# Configuration
AFFIDAVIT_FILE = Path("/home/ubuntu/canima/founding_affidavit/affidavit_clean.md")
OUTPUT_FILE = Path("/home/ubuntu/canima/AD_Paragraph_Order_Reference_144.txt")

def extract_ad_paragraphs(file_path):
    """Extract all paragraph numbers and their descriptions from the founding affidavit."""
    if not file_path.exists():
        print(f"Error: File not found at {file_path}")
        return []
    
    content = file_path.read_text()
    paragraphs = []
    
    # Find all paragraph numbers (e.g., 1.1, 3.4.2, 10.9.3.1)
    # Match patterns like: 1.1, 3.4.2, 10.9.3.1, etc.
    pattern = r'^(\d+(?:\.\d+)*)\s+(.+)$'
    
    for line in content.split('\n'):
        match = re.match(pattern, line.strip())
        if match:
            para_num = match.group(1)
            description = match.group(2).strip()
            # Clean up the description
            description = re.sub(r'\s+', ' ', description)
            paragraphs.append((para_num, description))
    
    return paragraphs

def generate_reference_file(paragraphs, output_path):
    """Generate the AD paragraph reference file."""
    with open(output_path, 'w') as f:
        f.write("AD Paragraph Numbers from Peter's Founding Affidavit (in order):\n")
        f.write("=" * 70 + "\n")
        
        for idx, (para_num, description) in enumerate(paragraphs, 1):
            # Truncate long descriptions
            if len(description) > 80:
                description = description[:77] + "..."
            f.write(f"{idx:3d}. AD {para_num} - {description}\n")
        
        f.write("\n" + "=" * 70 + "\n")
        f.write(f"Total: {len(paragraphs)} AD paragraphs\n")
    
    print(f"✓ Extracted {len(paragraphs)} AD paragraphs")
    print(f"✓ Saved to {output_path}")

def main():
    print("Extracting AD paragraphs from founding affidavit...")
    paragraphs = extract_ad_paragraphs(AFFIDAVIT_FILE)
    
    if paragraphs:
        generate_reference_file(paragraphs, OUTPUT_FILE)
    else:
        print("No paragraphs found!")

if __name__ == "__main__":
    main()

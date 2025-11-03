#!/usr/bin/env python3
"""Extract complete AD paragraph structure from founding affidavit."""

import re
import json

def extract_ad_paragraphs(file_path):
    """Extract all AD paragraphs with their content."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match paragraph numbers and their content
    # Matches: 1.1, 3.4.1, 10.7.1.2, etc.
    pattern = r'^(\d+(?:\.\d+)*)\s+(.+?)(?=^\d+(?:\.\d+)*\s|\Z)'
    
    paragraphs = []
    lines = content.split('\n')
    
    current_para = None
    current_content = []
    
    for line in lines:
        # Check if line starts with a paragraph number
        match = re.match(r'^(\d+(?:\.\d+)+)\s+(.*)$', line)
        if match:
            # Save previous paragraph
            if current_para:
                paragraphs.append({
                    'number': current_para,
                    'content': '\n'.join(current_content).strip()
                })
            # Start new paragraph
            current_para = match.group(1)
            current_content = [match.group(2)]
        elif current_para and line.strip():
            # Continue current paragraph
            current_content.append(line)
        elif current_para and not line.strip():
            # Empty line - might be end of paragraph or just spacing
            if current_content and current_content[-1] != '':
                current_content.append('')
    
    # Save last paragraph
    if current_para:
        paragraphs.append({
            'number': current_para,
            'content': '\n'.join(current_content).strip()
        })
    
    return paragraphs

def main():
    ad_file = '/home/ubuntu/canima/founding_affidavit/affidavit_clean.md'
    paragraphs = extract_ad_paragraphs(ad_file)
    
    # Save to JSON
    with open('/home/ubuntu/canima/ad_paragraphs_complete.json', 'w', encoding='utf-8') as f:
        json.dump(paragraphs, f, indent=2, ensure_ascii=False)
    
    print(f"Extracted {len(paragraphs)} AD paragraphs")
    
    # Print summary
    print("\nAD Paragraph Summary:")
    for para in paragraphs[:10]:
        print(f"  AD {para['number']}: {para['content'][:60]}...")
    
    # Save numbered list
    with open('/home/ubuntu/canima/ad_paragraphs_list.txt', 'w', encoding='utf-8') as f:
        for para in paragraphs:
            f.write(f"AD {para['number']}\n")
    
    print(f"\nSaved to:")
    print("  - ad_paragraphs_complete.json")
    print("  - ad_paragraphs_list.txt")

if __name__ == '__main__':
    main()

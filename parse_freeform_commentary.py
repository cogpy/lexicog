#!/usr/bin/env python3
"""
Parse and structure the free-form commentary from Jax's notes for AD paragraphs 7-10.
"""
import re
import json
from pathlib import Path

# --- Configuration ---
NOTES_FILE = Path("/home/ubuntu/canima/pasted_content_corrected.md")
OUTPUT_FILE = Path("/home/ubuntu/canima/analysis/freeform_commentary_ad_7_10.json")

def parse_freeform_commentary(notes_content):
    """Parse the free-form commentary from the notes for AD 7-10."""
    commentary_map = {}
    
    # Isolate the relevant sections (AD 7-10)
    section_7_match = re.search(r'## Section 4: Urgency and Alleged Misconduct \(AD 7-7.20\)(.*?)---', notes_content, re.DOTALL)
    section_8_9_match = re.search(r'## Section 5: Financial Discrepancies and Misconduct \(AD 8.4-9.3\)(.*?)---', notes_content, re.DOTALL)
    section_10_match = re.search(r'## Section 6: Application to Declare Respondents Delinquent \(AD 10.1-10.14\)(.*?)---', notes_content, re.DOTALL)

    sections_content = []
    if section_7_match:
        sections_content.append(section_7_match.group(1))
    if section_8_9_match:
        sections_content.append(section_8_9_match.group(1))
    if section_10_match:
        sections_content.append(section_10_match.group(1))

    full_section_content = "\n".join(sections_content)

    # Regex to find free-form comments associated with a paragraph number
    # Pattern: "7.1  (IMPORTANT + DETAIL LATER)\nMATERIAL NON-DISCLOSURE..."
    # This will capture multi-line comments until the next paragraph number or table
    pattern = re.compile(r'^([\d\.]+)\s+(.*?)(?=\n[\d\.]+\s+|^\||^---)', re.DOTALL | re.MULTILINE)

    matches = pattern.findall(full_section_content)

    for para_num, comment in matches:
        para_num = para_num.strip()
        comment = comment.strip()
        
        # Filter for AD 7-10 range
        if para_num.startswith('7.') or para_num.startswith('8.') or para_num.startswith('9.') or para_num.startswith('10.'):
            if para_num in commentary_map:
                commentary_map[para_num] += "\n" + comment
            else:
                commentary_map[para_num] = comment

    return commentary_map

def main():
    print("Parsing free-form commentary from Jax's notes...")
    
    if not NOTES_FILE.exists():
        print(f"Error: Notes file not found at {NOTES_FILE}")
        return

    notes_content = NOTES_FILE.read_text()
    commentary = parse_freeform_commentary(notes_content)

    if not commentary:
        print("No free-form commentary found for AD 7-10. Exiting.")
        return

    print(f"Found free-form commentary for {len(commentary)} AD paragraphs in the 7-10 range.")

    # Ensure the output directory exists
    OUTPUT_FILE.parent.mkdir(exist_ok=True)

    # Save the structured commentary to a JSON file
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(commentary, f, indent=2, sort_keys=True)
    
    print(f"✓ Saved structured commentary to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()


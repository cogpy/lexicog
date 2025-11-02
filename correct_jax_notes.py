#!/usr/bin/env python3
"""
Correct the AD paragraph numbers in Jax's notes using the mapping file.
"""
import re
import json
from pathlib import Path

# Configuration
NOTES_FILE_IN = Path("/home/ubuntu/upload/pasted_content.txt")
NOTES_FILE_OUT = Path("/home/ubuntu/canima/pasted_content_corrected.md")
MAPPING_FILE = Path("/home/ubuntu/canima/AD_Mapping_100_to_132.json")

def load_mapping(file_path):
    """Load the AD paragraph mapping from the JSON file."""
    if not file_path.exists():
        print(f"Error: Mapping file not found at {file_path}")
        return None
    with open(file_path, 'r') as f:
        return json.load(f)

def correct_notes(notes_content, mapping_data):
    """Correct the AD paragraph numbers in the notes content."""
    mapping = mapping_data.get("mapping", {})
    corrected_lines = []
    
    # Regex to find all occurrences of "AD X.Y" or "AD X.Y.Z"
    ad_para_pattern = re.compile(r'\*\*AD\s+([\d.]+)\*\*')

    for line in notes_content.split('\n'):
        # Find all matches in the line
        matches = list(ad_para_pattern.finditer(line))
        
        if not matches:
            corrected_lines.append(line)
            continue

        new_line = line
        # Iterate backwards to avoid index shifting during replacement
        for match in reversed(matches):
            old_para_num = match.group(1)
            
            # Check if this old number exists in our mapping
            if old_para_num in mapping:
                new_para_num = mapping[old_para_num]
                if new_para_num:
                    # Direct replacement
                    replacement = f"**AD {new_para_num}**"
                else:
                    # Paragraph was removed or renumbered
                    replacement = f"**[OLD AD {old_para_num} - REMOVED/RENUMBERED]**"
            else:
                # This AD number from the notes was not in the original 100-para list
                replacement = f"**[AD {old_para_num} - NOT IN 100-PARA REF]**"

            # Replace the specific match in the line
            start, end = match.span()
            new_line = new_line[:start] + replacement + new_line[end:]

        corrected_lines.append(new_line)
            
    return "\n".join(corrected_lines)

def main():
    print("Correcting AD paragraph numbers in Jax's notes...")
    
    # Load mapping
    mapping_data = load_mapping(MAPPING_FILE)
    if not mapping_data:
        return

    # Load notes
    if not NOTES_FILE_IN.exists():
        print(f"Error: Notes file not found at {NOTES_FILE_IN}")
        return
    notes_content = NOTES_FILE_IN.read_text()
    
    # Correct the notes
    corrected_content = correct_notes(notes_content, mapping_data)
    
    # Save the corrected notes
    NOTES_FILE_OUT.write_text(corrected_content)
    print(f"✓ Saved corrected notes to {NOTES_FILE_OUT}")

if __name__ == "__main__":
    main()


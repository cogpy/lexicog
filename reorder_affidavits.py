#!/usr/bin/env python3
"""
Reorder the v9 affidavits to fix the paragraph sequence and create v10.
"""
import re
from pathlib import Path

# --- Configuration ---
JR_AFFIDAVIT_V9 = Path("/home/ubuntu/canima/affidavits_refined/Jacqueline_Answering_Affidavit_v9_JR.md")
DR_AFFIDAVIT_V9 = Path("/home/ubuntu/canima/affidavits_refined/Daniel_Answering_Affidavit_v9_DR.md")
JR_AFFIDAVIT_V10 = Path("/home/ubuntu/canima/affidavits_refined/Jacqueline_Answering_Affidavit_v10_FINAL.md")
DR_AFFIDAVIT_V10 = Path("/home/ubuntu/canima/affidavits_refined/Daniel_Answering_Affidavit_v10_FINAL.md")

# --- Function to parse and sort affidavit sections ---
def reorder_affidavit(input_path, output_path, prefix):
    """Parses, sorts, and rewrites an affidavit to ensure correct paragraph order."""
    if not input_path.exists():
        print(f"Error: Input affidavit not found at {input_path}")
        return

    content = input_path.read_text()
    
    # Split the content into header and sections
    header_match = re.match(r"(.*?)(### .*)", content, re.DOTALL)
    if not header_match:
        print(f"Error: Could not find section headers in {input_path}")
        return
        
    header = header_match.group(1)
    body = header_match.group(2)
    
    # Find all sections (starting with ###)
    sections = re.split(r"(?=### )", body)
    
    # Create a dictionary to hold sections, keyed by the first paragraph number found
    section_map = {}
    for section in sections:
        if not section.strip():
            continue
        # Find the first JR/DR number in the section to use as a sort key
        match = re.search(r"\*\*{}\s+([\d.]+)".format(prefix), section)
        if match:
            para_num_str = match.group(1)
            # Use a tuple of integers for robust sorting (e.g., [7, 1] for 7.1)
            sort_key = tuple(map(int, para_num_str.split(".")))
            section_map[sort_key] = section
        else:
            # For sections without a JR/DR number (like intro), use a low-sorting key
            # This is a bit of a hack, assumes intro sections come first.
            # A more robust solution would be to handle them explicitly.
            section_map[(-1,)] = section # Keep intro at the top

    # Sort the sections based on the paragraph number key
    sorted_sections = [section_map[key] for key in sorted(section_map.keys())]
    
    # Combine header and sorted sections
    final_content = header + "".join(sorted_sections)
    
    output_path.write_text(final_content)
    print(f"✓ Successfully reordered and saved to {output_path}")

# --- Main Execution ---
def main():
    print("Starting affidavit reordering process...")
    reorder_affidavit(JR_AFFIDAVIT_V9, JR_AFFIDAVIT_V10, "JR")
    reorder_affidavit(DR_AFFIDAVIT_V9, DR_AFFIDAVIT_V10, "DR")
    print("\nAffidavit reordering complete.")

if __name__ == "__main__":
    main()


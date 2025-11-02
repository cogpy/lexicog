#!/usr/bin/env python3
"""
Integrate the extensive free-form commentary from Jax's notes for AD paragraphs 7-10
into the v11 affidavits to create comprehensive v12 versions.
"""
import re
import json
from pathlib import Path

# --- Configuration ---
COMMENTARY_FILE = Path("/home/ubuntu/canima/analysis/freeform_commentary_ad_7_10.json")
JR_AFFIDAVIT_IN = Path("/home/ubuntu/canima/affidavits_refined/Jacqueline_Answering_Affidavit_v11_FINAL.md")
DR_AFFIDAVIT_IN = Path("/home/ubuntu/canima/affidavits_refined/Daniel_Answering_Affidavit_v11_FINAL.md")
JR_AFFIDAVIT_OUT = Path("/home/ubuntu/canima/affidavits_refined/Jacqueline_Answering_Affidavit_v12_FINAL.md")
DR_AFFIDAVIT_OUT = Path("/home/ubuntu/canima/affidavits_refined/Daniel_Answering_Affidavit_v12_FINAL.md")

def load_commentary(file_path):
    """Load the commentary from the JSON file."""
    if not file_path.exists():
        print(f"Error: Commentary file not found at {file_path}")
        return {}
    with open(file_path, 'r') as f:
        return json.load(f)

def integrate_commentary(affidavit_content, commentary_map, prefix):
    """Integrate the commentary into the affidavit content."""
    enhanced_content = affidavit_content

    for para_num, commentary in commentary_map.items():
        # Find the section for the current AD paragraph
        para_pattern = re.compile(r'(\*\*{} {}\*\*)'.format(prefix, para_num))
        match = para_pattern.search(enhanced_content)

        if match:
            start_pos = match.end()
            # Find the end of the current paragraph block
            end_of_block_match = re.search(r'(\n\n|###|\*\*{} )'.format(prefix), enhanced_content[start_pos:])

            if end_of_block_match:
                insert_pos = start_pos + end_of_block_match.start()
            else:
                insert_pos = len(enhanced_content)

            # Format the commentary as a blockquote
            formatted_commentary = '\n'.join([f"> {line.strip()}\n>" for line in commentary.split('\n')])
            injection = f"\n\n**Detailed Commentary from Jax's Notes:**\n{formatted_commentary}\n"
            enhanced_content = enhanced_content[:insert_pos] + injection + enhanced_content[insert_pos:]
        else:
            print(f"Warning: AD paragraph {para_num} not found in the affidavit for {prefix}.")

    return enhanced_content

def main():
    print("Integrating free-form commentary into v11 affidavits...")

    commentary = load_commentary(COMMENTARY_FILE)
    if not commentary:
        print("No commentary found. Exiting.")
        return

    print(f"Loaded commentary for {len(commentary)} AD paragraphs.")

    # Enhance JR Affidavit
    if JR_AFFIDAVIT_IN.exists():
        jr_content = JR_AFFIDAVIT_IN.read_text()
        enhanced_jr = integrate_commentary(jr_content, commentary, "JR")
        JR_AFFIDAVIT_OUT.write_text(enhanced_jr)
        print(f"✓ Saved enhanced JR affidavit to {JR_AFFIDAVIT_OUT}")
    else:
        print(f"Error: JR affidavit not found at {JR_AFFIDAVIT_IN}")

    # Enhance DR Affidavit
    if DR_AFFIDAVIT_IN.exists():
        dr_content = DR_AFFIDAVIT_IN.read_text()
        enhanced_dr = integrate_commentary(dr_content, commentary, "DR")
        DR_AFFIDAVIT_OUT.write_text(enhanced_dr)
        print(f"✓ Saved enhanced DR affidavit to {DR_AFFIDAVIT_OUT}")
    else:
        print(f"Error: DR affidavit not found at {DR_AFFIDAVIT_IN}")

if __name__ == "__main__":
    main()


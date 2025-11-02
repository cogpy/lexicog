#!/usr/bin/env python3
"""
Enhance the v10 final affidavits with the commentary from Jax's corrected notes.
"""
import re
from pathlib import Path

# --- Configuration ---
NOTES_FILE = Path("/home/ubuntu/canima/pasted_content_corrected.md")
JR_AFFIDAVIT_IN = Path("/home/ubuntu/canima/affidavits_refined/Jacqueline_Answering_Affidavit_v10_FINAL.md")
DR_AFFIDAVIT_IN = Path("/home/ubuntu/canima/affidavits_refined/Daniel_Answering_Affidavit_v10_FINAL.md")
JR_AFFIDAVIT_OUT = Path("/home/ubuntu/canima/affidavits_refined/Jacqueline_Answering_Affidavit_v11_FINAL.md")
DR_AFFIDAVIT_OUT = Path("/home/ubuntu/canima/affidavits_refined/Daniel_Answering_Affidavit_v11_FINAL.md")

def parse_jax_notes(notes_path):
    """Parse Jax's notes and extract commentary for each AD paragraph."""
    if not notes_path.exists():
        print(f"Error: Notes file not found at {notes_path}")
        return {}
    
    content = notes_path.read_text()
    commentary_map = {}
    
    # Split by sections first
    sections = re.split(r'## Section \d+:', content)[1:] # Skip intro
    
    for section in sections:
        # Find all table rows
        rows = re.findall(r'\| \*\*AD ([\d.]+)\*\*.*? \| (.*?)\|', section, re.DOTALL)
        for para_num, commentary in rows:
            para_num = para_num.strip()
            commentary = commentary.strip()
            if commentary and commentary != "AGREED":
                commentary_map[para_num] = commentary

        # Also capture free-form commentary not in tables
        free_form_comments = re.findall(r'^([\d.]+)\s+(.*)', section, re.MULTILINE)
        for para_num, comment in free_form_comments:
            para_num = para_num.strip()
            comment = comment.strip()
            if para_num in commentary_map:
                commentary_map[para_num] += "\n" + comment
            else:
                commentary_map[para_num] = comment

    return commentary_map

def enhance_affidavit(affidavit_content, commentary_map, prefix):
    """Enhance the affidavit content with commentary from Jax's notes."""
    enhanced_content = affidavit_content
    
    for para_num, commentary in commentary_map.items():
        # Find the section for the current AD paragraph
        # Pattern: "**JR 1.1**"
        para_pattern = re.compile(r'(\*\*{} {}\*\*)'.format(prefix, para_num))
        match = para_pattern.search(enhanced_content)
        
        if match:
            # Found the paragraph, let's append the commentary
            start_pos = match.end()
            # Find the end of the current paragraph block (next heading or double newline)
            end_of_block_match = re.search(r'(\n\n|###|\*\*{} )'.format(prefix), enhanced_content[start_pos:])
            
            if end_of_block_match:
                insert_pos = start_pos + end_of_block_match.start()
            else:
                insert_pos = len(enhanced_content) # Append at the end if no clear end found

            # Inject the commentary
            formatted_commentary = commentary.replace('\n', '\n> ')
            injection = f"\n\n**Jax\'s Notes:**\n> {formatted_commentary}\n"
            enhanced_content = enhanced_content[:insert_pos] + injection + enhanced_content[insert_pos:]
        else:
            # If the paragraph doesn't exist, we might need to add it.
            # For now, we'll just print a warning.
            print(f"Warning: AD paragraph {para_num} not found in the affidavit for {prefix}.")
            
    return enhanced_content

def main():
    print("Enhancing affidavits with Jax's notes...")
    
    # Parse notes
    commentary = parse_jax_notes(NOTES_FILE)
    if not commentary:
        print("No commentary found in notes. Exiting.")
        return
    
    print(f"Found commentary for {len(commentary)} AD paragraphs.")

    # Enhance JR Affidavit
    if JR_AFFIDAVIT_IN.exists():
        jr_content = JR_AFFIDAVIT_IN.read_text()
        enhanced_jr = enhance_affidavit(jr_content, commentary, "JR")
        JR_AFFIDAVIT_OUT.write_text(enhanced_jr)
        print(f"✓ Saved enhanced JR affidavit to {JR_AFFIDAVIT_OUT}")
    else:
        print(f"Error: JR affidavit not found at {JR_AFFIDAVIT_IN}")

    # Enhance DR Affidavit
    if DR_AFFIDAVIT_IN.exists():
        dr_content = DR_AFFIDAVIT_IN.read_text()
        enhanced_dr = enhance_affidavit(dr_content, commentary, "DR")
        DR_AFFIDAVIT_OUT.write_text(enhanced_dr)
        print(f"✓ Saved enhanced DR affidavit to {DR_AFFIDAVIT_OUT}")
    else:
        print(f"Error: DR affidavit not found at {DR_AFFIDAVIT_IN}")

if __name__ == "__main__":
    main()


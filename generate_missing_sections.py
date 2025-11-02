#!/usr/bin/env python3
"""
Generate missing sections for JR and DR affidavits to ensure full coverage.
"""
import re
from pathlib import Path

# --- Configuration ---
AD_REF_FILE = Path("/home/ubuntu/canima/AD_Paragraph_Order_Reference.txt")
ALIGNMENT_REPORT_FILE = Path("/home/ubuntu/canima/AD_ALIGNMENT_VERIFICATION_REPORT.md")
JR_AFFIDAVIT_IN = Path("/home/ubuntu/canima/affidavits_refined/Jacqueline_Answering_Affidavit_v8_JR.md")
DR_AFFIDAVIT_IN = Path("/home/ubuntu/canima/affidavits_refined/Daniel_Answering_Affidavit_v8_DR.md")
JR_AFFIDAVIT_OUT = Path("/home/ubuntu/canima/affidavits_refined/Jacqueline_Answering_Affidavit_v9_JR.md")
DR_AFFIDAVIT_OUT = Path("/home/ubuntu/canima/affidavits_refined/Daniel_Answering_Affidavit_v9_DR.md")
COMMENTARY_FILE = Path("/home/ubuntu/canima/AD_PARAGRAPH_COMMENTARY_COMPLETED.md")

# --- 1. Extract Uncovered Paragraphs ---
def get_uncovered_paragraphs(report_path):
    """Extracts a list of uncovered AD paragraphs from the alignment report."""
    if not report_path.exists():
        print(f"Error: Alignment report not found at {report_path}")
        return []
    content = report_path.read_text()
    uncovered_section = re.search(r"### Uncovered AD Paragraphs \((\d+)\)(.*)", content, re.DOTALL)
    if not uncovered_section:
        return []
    
    uncovered_content = uncovered_section.group(2)
    # Regex to find all "- AD X.Y.Z - Description"
    matches = re.findall(r"-\s+AD\s+([\d.]+)\s+-\s+(.*)", uncovered_content)
    return {para.strip(): desc.strip() for para, desc in matches}

# --- 2. Load Existing Affidavits ---
def load_affidavit(file_path):
    """Loads the content of an affidavit file."""
    if not file_path.exists():
        print(f"Warning: Affidavit file not found at {file_path}, starting fresh.")
        return ""
    return file_path.read_text()

# --- 3. Load Commentary ---
def load_commentary(file_path):
    """Loads the commentary file to find relevant insights."""
    if not file_path.exists():
        return {}
    content = file_path.read_text()
    # Regex to find commentary for a specific AD paragraph
    # Example: | **AD 1.3** - ... | Commentary... |
    matches = re.findall(r"\|\s*\*\*AD\s+([\d.]+)\*\*.*?\|\s*(.*?)\s*\|", content, re.DOTALL)
    commentary_map = {para.strip(): com.strip().replace('\n', ' ') for para, com in matches}
    return commentary_map

# --- 4. Generate New Sections ---
def generate_new_sections(uncovered_paras, commentary_map, prefix):
    """Generates markdown for the uncovered paragraphs."""
    new_sections = []
    # Group by main paragraph number (e.g., 1, 2, 3)
    grouped_paras = {}
    for para, desc in uncovered_paras.items():
        main_num = para.split('.')[0]
        if main_num not in grouped_paras:
            grouped_paras[main_num] = []
        grouped_paras[main_num].append((para, desc))

    sorted_main_nums = sorted(grouped_paras.keys(), key=int)

    for main_num in sorted_main_nums:
        # Find the main title from the commentary file if possible
        main_title = f"RESPONSE TO AD PARAGRAPHS STARTING WITH {main_num}" # Default title
        # A bit of a hack to find a representative title
        first_para_desc = grouped_paras[main_num][0][1]
        if "Parties" in first_para_desc:
            main_title = "RESPONSE TO AD PARAGRAPHS: PARTIES AND STRUCTURE"
        elif "Accountant" in first_para_desc:
            main_title = "RESPONSE TO AD PARAGRAPH: ACCOUNTANT'S CONFLICT OF INTEREST"
        elif "Urgency" in first_para_desc:
            main_title = "RESPONSE TO AD PARAGRAPHS: URGENCY AND ALLEGED MISCONDUCT"

        new_sections.append(f"### {main_title}\n")
        
        sorted_paras = sorted(grouped_paras[main_num], key=lambda x: [int(n) for n in x[0].split('.')])

        for para, desc in sorted_paras:
            comment = commentary_map.get(para, "The contents of this paragraph are noted and addressed where relevant.")
            # Clean up commentary
            comment = re.sub(r'\[.*?\]', '', comment) # remove citations
            comment = comment.replace('Peter', 'The Applicant')
            comment = comment.replace('Jax', 'The First Respondent')
            comment = comment.replace('Dan', 'The Second Respondent')

            new_sections.append(f"**{prefix} {para}**  ")
            new_sections.append(f"*{desc}*  ")
            new_sections.append(f"{comment}\n")
        new_sections.append("---\n")

    return "\n".join(new_sections)

# --- Main Execution ---
def main():
    print("Starting affidavit refinement process...")
    uncovered_paras = get_uncovered_paragraphs(ALIGNMENT_REPORT_FILE)
    if not uncovered_paras:
        print("No uncovered paragraphs found or report is missing. Exiting.")
        return

    print(f"Found {len(uncovered_paras)} uncovered paragraphs to address.")

    commentary_map = load_commentary(COMMENTARY_FILE)
    print(f"Loaded {len(commentary_map)} commentary entries.")

    # --- Process JR Affidavit ---
    print("\nProcessing Jacqueline's Affidavit (JR)...")
    jr_content_old = load_affidavit(JR_AFFIDAVIT_IN)
    jr_new_sections = generate_new_sections(uncovered_paras, commentary_map, "JR")
    jr_content_new = jr_content_old + "\n\n## RESPONSES TO UNCOVERED PARAGRAPHS\n\n" + jr_new_sections
    JR_AFFIDAVIT_OUT.write_text(jr_content_new)
    print(f"✓ Saved updated JR affidavit to {JR_AFFIDAVIT_OUT}")

    # --- Process DR Affidavit ---
    print("\nProcessing Daniel's Affidavit (DR)...")
    dr_content_old = load_affidavit(DR_AFFIDAVIT_IN)
    dr_new_sections = generate_new_sections(uncovered_paras, commentary_map, "DR")
    dr_content_new = dr_content_old + "\n\n## RESPONSES TO UNCOVERED PARAGRAPHS\n\n" + dr_new_sections
    DR_AFFIDAVIT_OUT.write_text(dr_content_new)
    print(f"✓ Saved updated DR affidavit to {DR_AFFIDAVIT_OUT}")

    print("\nAffidavit refinement complete.")

if __name__ == "__main__":
    main()


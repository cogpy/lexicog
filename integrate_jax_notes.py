#!/usr/bin/env python3
"""
Integrate Jax's AD notes into Jacqueline's refined affidavit (v13) to create v14.
"""
import re
from pathlib import Path

def load_jax_notes():
    """Load structured commentary from JAX_AD_NOTES.md using line-by-line parsing"""
    notes_file = Path('/home/ubuntu/canima/JAX_AD_NOTES.md')
    notes = {}
    in_table = False
    with open(notes_file, 'r') as f:
        for line in f:
            if "|:--------|:------|:-----------------|" in line:
                in_table = True
                continue
            if "### Key Points" in line:
                in_table = False
                continue
            
            if in_table and line.startswith("| AD"):
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 4:
                    para_num_match = re.search(r"AD ([\d.-]+)", parts[1])
                    if para_num_match:
                        para_num = para_num_match.group(1)
                        commentary = parts[3]
                        notes[para_num] = commentary
    return notes

def main():
    base_path = Path('/home/ubuntu/canima')
    refined_affidavit_path = base_path / 'affidavits_refined' / 'Jacqueline_Answering_Affidavit_v13_REFINED.md'
    output_affidavit_path = base_path / 'affidavits_refined' / 'Jacqueline_Answering_Affidavit_v14_INTEGRATED.md'

    jax_notes = load_jax_notes()

    with open(refined_affidavit_path, 'r') as f:
        content = f.read()

    def replace_response(match):
        para_num = match.group(1)
        response_text = match.group(2).strip()

        if para_num in jax_notes:
            new_response = jax_notes[para_num]
            # Add a placeholder for the annexure citation
            response_text = f"{new_response} [Annexure JR-{para_num}]"
        elif "[Annexure JR-X]" in response_text:
            response_text = response_text.replace("[Annexure JR-X]", f"[Annexure JR-{para_num}]")
        
        return f"**JR {para_num}**\n\n{response_text}"

    pattern = re.compile(r'\*\*JR (\d[\d.]*)\*\*\n\n(.*?)(?=\n\*\*JR|\Z)', re.DOTALL)
    integrated_content = pattern.sub(replace_response, content)
    
    integrated_content = integrated_content.replace(
        "# Answering Affidavit of Jacqueline Faucitt (v13 - Refined)",
        "# Answering Affidavit of Jacqueline Faucitt (v14 - Integrated)"
    )

    with open(output_affidavit_path, 'w') as f:
        f.write(integrated_content)

    print(f"Integration complete. New affidavit saved to: {output_affidavit_path}")
    print(f"Integrated {len(jax_notes)} notes into the affidavit.")

if __name__ == '__main__':
    main()

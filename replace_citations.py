#!/usr/bin/env python3
"""
Replace citation placeholders in Jacqueline's affidavit with full annexure descriptions.
"""
import re
import json
from pathlib import Path

def main():
    base_path = Path('/home/ubuntu/canima')
    affidavit_path = base_path / 'affidavits_refined' / 'Jacqueline_Answering_Affidavit_v14_INTEGRATED.md'
    output_path = base_path / 'affidavits_refined' / 'Jacqueline_Answering_Affidavit_v15_CITED.md'
    annexure_path = base_path / 'ANNEXURE_DESCRIPTIONS_JR_COMPREHENSIVE.json'

    with open(annexure_path, 'r') as f:
        annexure_map = json.load(f)

    with open(affidavit_path, 'r') as f:
        content = f.read()

    def replace_citation(match):
        placeholder = match.group(0)
        annexure_id_full = match.group(1)  # e.g., "Annexure JR-1.3"
        annexure_id = annexure_id_full.replace("Annexure ", "")  # e.g., "JR-1.3"
        
        if annexure_id in annexure_map:
            description = annexure_map[annexure_id]
            return f'[{annexure_id}, {description}]'
        else:
            # If no description is found, keep the original placeholder but format it consistently
            return f'[{annexure_id}]'

    # Regex to find all placeholders like [Annexure JR-1.1]
    pattern = re.compile(r'\[(Annexure JR-[\d.]+)\]')
    cited_content = pattern.sub(replace_citation, content)
    
    # Update the title
    cited_content = cited_content.replace(
        "# Answering Affidavit of Jacqueline Faucitt (v14 - Integrated)",
        "# Answering Affidavit of Jacqueline Faucitt (v15 - Cited)"
    )

    with open(output_path, 'w') as f:
        f.write(cited_content)

    print(f"Citation replacement complete. New affidavit saved to: {output_path}")

if __name__ == '__main__':
    main()


#!/usr/bin/env python3
"""
Verify that citations have been properly replaced in Jacqueline's affidavit.
"""
import re
from pathlib import Path

def main():
    base_path = Path('/home/ubuntu/canima/affidavits_refined')
    affidavit_path = base_path / 'Jacqueline_Answering_Affidavit_v15_CITED.md'

    with open(affidavit_path, 'r') as f:
        content = f.read()

    # Find all citations
    all_citations = re.findall(r'\[(?:Annexure )?JR-[\d.]+(?:,.*?)?\]', content)
    
    # Find citations with descriptions (contain comma)
    cited_with_description = [c for c in all_citations if ',' in c]
    
    # Find citations without descriptions (no comma)
    cited_without_description = [c for c in all_citations if ',' not in c]
    
    # Count unique citations
    unique_citations = set(all_citations)
    
    print(f"Citation Verification Report")
    print(f"=" * 60)
    print(f"\nTotal citations found: {len(all_citations)}")
    print(f"Unique citations: {len(unique_citations)}")
    print(f"Citations with descriptions: {len(cited_with_description)}")
    print(f"Citations without descriptions: {len(cited_without_description)}")
    
    if cited_without_description:
        print(f"\n⚠️  Citations still needing descriptions:")
        for citation in sorted(set(cited_without_description)):
            print(f"  - {citation}")
    else:
        print(f"\n✓ All citations have descriptions!")
    
    # Sample some citations with descriptions
    if cited_with_description:
        print(f"\n✓ Sample citations with descriptions:")
        for citation in sorted(set(cited_with_description))[:5]:
            print(f"  - {citation}")

if __name__ == '__main__':
    main()


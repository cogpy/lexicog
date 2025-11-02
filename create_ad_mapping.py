#!/usr/bin/env python3
"""
Create a mapping between the old 100-paragraph AD reference and the new 132-paragraph structure.
"""
import re
from pathlib import Path
import json

# Configuration
OLD_REF_FILE = Path("/home/ubuntu/canima/AD_Paragraph_Order_Reference.txt")
NEW_REF_FILE = Path("/home/ubuntu/canima/AD_Paragraph_Order_Reference_132.txt")
OUTPUT_MAPPING_FILE = Path("/home/ubuntu/canima/AD_Mapping_100_to_132.json")
OUTPUT_REPORT_FILE = Path("/home/ubuntu/canima/AD_Mapping_Report.md")

def parse_reference_file(file_path):
    """Parse an AD reference file and return a list of (index, para_num, description) tuples."""
    if not file_path.exists():
        print(f"Error: File not found at {file_path}")
        return []
    
    content = file_path.read_text()
    paragraphs = []
    
    # Pattern: "  1. AD 1 - Description"
    pattern = r'^\s*(\d+)\.\s+AD\s+([\d.]+)\s+-\s+(.+)$'
    
    for line in content.split('\n'):
        match = re.match(pattern, line)
        if match:
            index = int(match.group(1))
            para_num = match.group(2)
            description = match.group(3).strip()
            paragraphs.append((index, para_num, description))
    
    return paragraphs

def create_mapping(old_paras, new_paras):
    """Create a mapping between old and new AD paragraph numbers."""
    mapping = {}
    reverse_mapping = {}
    
    # Create dictionaries for quick lookup
    old_dict = {para_num: (idx, desc) for idx, para_num, desc in old_paras}
    new_dict = {para_num: (idx, desc) for idx, para_num, desc in new_paras}
    
    # Find paragraphs that exist in both
    for para_num in old_dict:
        if para_num in new_dict:
            mapping[para_num] = para_num  # Same number in both
        else:
            # This paragraph number doesn't exist in the new structure
            # We need to find the closest match or mark as removed
            mapping[para_num] = None
    
    # Find new paragraphs that didn't exist in old structure
    new_only = []
    for para_num in new_dict:
        if para_num not in old_dict:
            new_only.append(para_num)
            reverse_mapping[para_num] = "NEW"
    
    return mapping, new_only

def generate_report(old_paras, new_paras, mapping, new_only):
    """Generate a human-readable report of the mapping."""
    report = f"""# AD Paragraph Mapping Report: 100 → 132 Structure

**Date:** November 2, 2025

## Summary

- **Old structure:** {len(old_paras)} AD paragraphs
- **New structure:** {len(new_paras)} AD paragraphs
- **New paragraphs added:** {len(new_only)}
- **Paragraphs unchanged:** {sum(1 for v in mapping.values() if v is not None)}
- **Paragraphs removed/renumbered:** {sum(1 for v in mapping.values() if v is None)}

---

## New AD Paragraphs (Not in Old Structure)

The following {len(new_only)} AD paragraphs are new in the 132-paragraph structure:

"""
    
    new_dict = {para_num: (idx, desc) for idx, para_num, desc in new_paras}
    
    for para_num in sorted(new_only, key=lambda x: [int(n) for n in x.split('.')]):
        idx, desc = new_dict[para_num]
        report += f"- **AD {para_num}** (#{idx}) - {desc[:80]}{'...' if len(desc) > 80 else ''}\n"
    
    report += "\n---\n\n"
    report += "## Mapping Details\n\n"
    report += "### Old → New Mapping\n\n"
    
    old_dict = {para_num: (idx, desc) for idx, para_num, desc in old_paras}
    
    for para_num in sorted(mapping.keys(), key=lambda x: [int(n) for n in x.split('.')]):
        old_idx, old_desc = old_dict[para_num]
        new_para = mapping[para_num]
        if new_para:
            report += f"- **AD {para_num}** → **AD {new_para}** (unchanged)\n"
        else:
            report += f"- **AD {para_num}** → **REMOVED/RENUMBERED**\n"
    
    return report

def main():
    print("Creating AD paragraph mapping...")
    
    # Parse both reference files
    old_paras = parse_reference_file(OLD_REF_FILE)
    new_paras = parse_reference_file(NEW_REF_FILE)
    
    if not old_paras or not new_paras:
        print("Error: Could not parse reference files")
        return
    
    print(f"Old structure: {len(old_paras)} paragraphs")
    print(f"New structure: {len(new_paras)} paragraphs")
    
    # Create mapping
    mapping, new_only = create_mapping(old_paras, new_paras)
    
    # Save mapping as JSON
    mapping_data = {
        "old_count": len(old_paras),
        "new_count": len(new_paras),
        "mapping": mapping,
        "new_paragraphs": new_only
    }
    
    with open(OUTPUT_MAPPING_FILE, 'w') as f:
        json.dump(mapping_data, f, indent=2)
    
    print(f"✓ Saved mapping to {OUTPUT_MAPPING_FILE}")
    
    # Generate report
    report = generate_report(old_paras, new_paras, mapping, new_only)
    OUTPUT_REPORT_FILE.write_text(report)
    
    print(f"✓ Saved report to {OUTPUT_REPORT_FILE}")
    print(f"✓ Found {len(new_only)} new AD paragraphs")

if __name__ == "__main__":
    main()

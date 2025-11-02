#!/usr/bin/env python3
"""
Verify AD paragraph alignment and coverage in JR/DR affidavits
"""
import re
from pathlib import Path
from collections import defaultdict

# Read the AD paragraph order reference
ad_ref_file = Path("/home/ubuntu/canima/AD_Paragraph_Order_Reference.txt")
ad_content = ad_ref_file.read_text()

# Extract AD paragraphs from the reference file
ad_paragraphs = []
for line in ad_content.split('\n'):
    match = re.search(r'^\s*\d+\.\s+(AD\s+[\d.]+)', line)
    if match:
        ad_para = match.group(1).replace('AD ', '').strip()
        ad_paragraphs.append(ad_para)

print(f"Found {len(ad_paragraphs)} AD paragraphs in reference file")

# Read JR affidavit
jr_file = Path("/home/ubuntu/canima/affidavits_refined/Jacqueline_Answering_Affidavit_v8_JR.md")
jr_content = jr_file.read_text() if jr_file.exists() else ""

# Read DR affidavit
dr_file = Path("/home/ubuntu/canima/affidavits_refined/Daniel_Answering_Affidavit_v8_DR.md")
dr_content = dr_file.read_text() if dr_file.exists() else ""

# Extract JR references
jr_refs = set(re.findall(r'JR\s+([\d.]+)', jr_content))
print(f"Found {len(jr_refs)} unique JR references")

# Extract DR references
dr_refs = set(re.findall(r'DR\s+([\d.]+)', dr_content))
print(f"Found {len(dr_refs)} unique DR references")

# Check coverage
covered_by_jr = set()
covered_by_dr = set()
covered_by_both = set()
uncovered = set()

for ad_para in ad_paragraphs:
    in_jr = ad_para in jr_refs
    in_dr = ad_para in dr_refs
    
    if in_jr and in_dr:
        covered_by_both.add(ad_para)
    elif in_jr:
        covered_by_jr.add(ad_para)
    elif in_dr:
        covered_by_dr.add(ad_para)
    else:
        uncovered.add(ad_para)

# Generate report
report = f"""# AD Paragraph Coverage and Alignment Report

**Date:** November 2, 2025

## Summary

- **Total AD paragraphs:** {len(ad_paragraphs)}
- **Covered by JR only:** {len(covered_by_jr)}
- **Covered by DR only:** {len(covered_by_dr)}
- **Covered by both JR and DR:** {len(covered_by_both)}
- **Total covered:** {len(covered_by_jr) + len(covered_by_dr) + len(covered_by_both)}
- **Uncovered:** {len(uncovered)}
- **Coverage percentage:** {((len(covered_by_jr) + len(covered_by_dr) + len(covered_by_both)) / len(ad_paragraphs) * 100):.1f}%

## Coverage Details

### Covered by JR Only ({len(covered_by_jr)})
"""

for para in sorted(covered_by_jr, key=lambda x: [int(n) for n in x.split('.')]):
    report += f"- AD {para}\n"

report += f"\n### Covered by DR Only ({len(covered_by_dr)})\n"
for para in sorted(covered_by_dr, key=lambda x: [int(n) for n in x.split('.')]):
    report += f"- AD {para}\n"

report += f"\n### Covered by Both JR and DR ({len(covered_by_both)})\n"
for para in sorted(covered_by_both, key=lambda x: [int(n) for n in x.split('.')]):
    report += f"- AD {para}\n"

report += f"\n### Uncovered AD Paragraphs ({len(uncovered)})\n"
for para in sorted(uncovered, key=lambda x: [int(n) for n in x.split('.')]):
    # Find the description from the reference file
    desc = ""
    for line in ad_content.split('\n'):
        if f"AD {para}" in line:
            desc = line.split('-', 1)[1].strip() if '-' in line else ""
            break
    report += f"- AD {para} - {desc}\n"

# Check for order violations
report += f"\n## Order Verification\n\n"

def extract_ad_sequence(content, prefix):
    """Extract AD paragraph numbers in the order they appear"""
    pattern = f"{prefix}\\s+([\\d.]+)"
    matches = re.findall(pattern, content)
    return matches

jr_sequence = extract_ad_sequence(jr_content, "JR")
dr_sequence = extract_ad_sequence(dr_content, "DR")

def check_order(sequence, prefix):
    """Check if AD paragraphs appear in correct order"""
    violations = []
    for i in range(len(sequence) - 1):
        current = [int(n) for n in sequence[i].split('.')]
        next_para = [int(n) for n in sequence[i+1].split('.')]
        
        # Check if next is greater than or equal to current
        if next_para < current:
            violations.append((sequence[i], sequence[i+1]))
    
    return violations

jr_violations = check_order(jr_sequence, "JR")
dr_violations = check_order(dr_sequence, "DR")

report += f"### JR Affidavit Order\n"
if jr_violations:
    report += f"**⚠ Found {len(jr_violations)} order violations:**\n\n"
    for v1, v2 in jr_violations:
        report += f"- JR {v1} followed by JR {v2} (out of order)\n"
else:
    report += "✓ All JR references appear in correct order\n"

report += f"\n### DR Affidavit Order\n"
if dr_violations:
    report += f"**⚠ Found {len(dr_violations)} order violations:**\n\n"
    for v1, v2 in dr_violations:
        report += f"- DR {v1} followed by DR {v2} (out of order)\n"
else:
    report += "✓ All DR references appear in correct order\n"

# Save report
output_file = Path("/home/ubuntu/canima/AD_ALIGNMENT_VERIFICATION_REPORT.md")
output_file.write_text(report)

print(f"\n✓ Report saved to {output_file}")
print(f"\nCoverage: {len(covered_by_jr) + len(covered_by_dr) + len(covered_by_both)}/{len(ad_paragraphs)} ({((len(covered_by_jr) + len(covered_by_dr) + len(covered_by_both)) / len(ad_paragraphs) * 100):.1f}%)")
print(f"Uncovered: {len(uncovered)}")

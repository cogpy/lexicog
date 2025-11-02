#!/usr/bin/env python3
"""
Verify the v10 final affidavits for 100% coverage and correct order.
"""
import re
from pathlib import Path

# --- Configuration ---
AD_REF_FILE = Path("/home/ubuntu/canima/AD_Paragraph_Order_Reference.txt")
JR_AFFIDAVIT_V10 = Path("/home/ubuntu/canima/affidavits_refined/Jacqueline_Answering_Affidavit_v10_FINAL.md")
DR_AFFIDAVIT_V10 = Path("/home/ubuntu/canima/affidavits_refined/Daniel_Answering_Affidavit_v10_FINAL.md")
OUTPUT_REPORT_FILE = Path("/home/ubuntu/canima/AD_ALIGNMENT_VERIFICATION_REPORT_V10_FINAL.md")

# --- Functions (copied from previous script) ---
def get_ad_paragraphs(ref_path):
    if not ref_path.exists(): return []
    content = ref_path.read_text()
    return [match.group(1).replace('AD ', '').strip() for match in re.finditer(r'^\s*\d+\.\s+(AD\s+[\d.]+)', content, re.MULTILINE)]

def get_references(file_path, prefix):
    if not file_path.exists(): return set()
    content = file_path.read_text()
    # Updated regex to find references within sections
    return set(re.findall(r'\*\*{}\s+([\d.]+)'.format(prefix), content))

def check_order(file_path, prefix):
    if not file_path.exists(): return []
    content = file_path.read_text()
    # This regex needs to be robust enough to handle the structure
    # It should find all occurrences of the pattern in the document order
    sequence = re.findall(r'\*\*{}\s+([\d.]+)'.format(prefix), content)
    violations = []
    # Convert to sortable keys
    sortable_sequence = [tuple(map(int, s.split('.'))) for s in sequence]
    
    for i in range(len(sortable_sequence) - 1):
        if sortable_sequence[i+1] < sortable_sequence[i]:
            violations.append((sequence[i], sequence[i+1]))
    return violations

def generate_report(ad_paras, jr_refs, dr_refs, jr_violations, dr_violations):
    all_refs = jr_refs.union(dr_refs)
    uncovered = set(ad_paras) - all_refs
    total_covered = len(ad_paras) - len(uncovered)
    coverage_percentage = (total_covered / len(ad_paras) * 100) if ad_paras else 0

    report = f"""# V10 FINAL AD Paragraph Coverage and Alignment Report

**Date:** November 2, 2025

## Summary

- **Total AD paragraphs:** {len(ad_paras)}
- **Total covered:** {total_covered}
- **Uncovered:** {len(uncovered)}
- **Coverage percentage:** {coverage_percentage:.1f}%

"""

    if uncovered:
        report += f"## ⚠ Uncovered AD Paragraphs ({len(uncovered)})\n"
        for para in sorted(uncovered, key=lambda x: [int(n) for n in x.split('.')]):
            report += f"- AD {para}\n"
    else:
        report += "## ✓ All AD Paragraphs Covered\n"

    report += "\n## Order Verification\n"
    report += "\n### JR Affidavit Order\n"
    if jr_violations:
        report += f"**⚠ Found {len(jr_violations)} order violations:**\n\n"
        for v1, v2 in jr_violations:
            report += f"- JR {v1} followed by JR {v2} (out of order)\n"
    else:
        report += "✓ All JR references appear in correct order.\n"

    report += f"\n### DR Affidavit Order\n"
    if dr_violations:
        report += f"**⚠ Found {len(dr_violations)} order violations:**\n\n"
        for v1, v2 in dr_violations:
            report += f"- DR {v1} followed by DR {v2} (out of order)\n"
    else:
        report += "✓ All DR references appear in correct order.\n"
        
    return report

# --- Main Execution ---
def main():
    print("Starting v10 FINAL affidavit verification...")
    ad_paragraphs = get_ad_paragraphs(AD_REF_FILE)
    jr_references = get_references(JR_AFFIDAVIT_V10, "JR")
    dr_references = get_references(DR_AFFIDAVIT_V10, "DR")
    
    jr_order_violations = check_order(JR_AFFIDAVIT_V10, "JR")
    dr_order_violations = check_order(DR_AFFIDAVIT_V10, "DR")

    report_content = generate_report(ad_paragraphs, jr_references, dr_references, jr_order_violations, dr_order_violations)

    OUTPUT_REPORT_FILE.write_text(report_content)
    print(f"✓ Verification complete. Report saved to {OUTPUT_REPORT_FILE}")

if __name__ == "__main__":
    main()


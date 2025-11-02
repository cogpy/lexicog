#!/usr/bin/env python3
"""
Verify AD paragraph alignment and coverage in the v9 JR/DR affidavits
"""
import re
from pathlib import Path

# --- Configuration ---
AD_REF_FILE = Path("/home/ubuntu/canima/AD_Paragraph_Order_Reference.txt")
JR_AFFIDAVIT_V9 = Path("/home/ubuntu/canima/affidavits_refined/Jacqueline_Answering_Affidavit_v9_JR.md")
DR_AFFIDAVIT_V9 = Path("/home/ubuntu/canima/affidavits_refined/Daniel_Answering_Affidavit_v9_DR.md")
OUTPUT_REPORT_FILE = Path("/home/ubuntu/canima/AD_ALIGNMENT_VERIFICATION_REPORT_V9.md")

# --- 1. Extract AD Paragraphs from Reference ---
def get_ad_paragraphs(ref_path):
    if not ref_path.exists():
        return []
    content = ref_path.read_text()
    ad_paragraphs = []
    for line in content.split('\n'):
        match = re.search(r'^\s*\d+\.\s+(AD\s+[\d.]+)', line)
        if match:
            ad_para = match.group(1).replace('AD ', '').strip()
            ad_paragraphs.append(ad_para)
    return ad_paragraphs

# --- 2. Extract JR/DR References from Affidavits ---
def get_references(file_path, prefix):
    if not file_path.exists():
        return set()
    content = file_path.read_text()
    return set(re.findall(r'\*\*{}\s+([\d.]+)'.format(prefix), content))

# --- 3. Check Coverage ---
def check_coverage(ad_paras, jr_refs, dr_refs):
    covered_by_jr = set()
    covered_by_dr = set()
    covered_by_both = set()
    uncovered = set()

    for ad_para in ad_paras:
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
            
    return covered_by_jr, covered_by_dr, covered_by_both, uncovered

# --- 4. Check Order ---
def check_order(file_path, prefix):
    if not file_path.exists():
        return []
    content = file_path.read_text()
    sequence = re.findall(r'\*\*{}\s+([\d.]+)'.format(prefix), content)
    violations = []
    for i in range(len(sequence) - 1):
        current = [int(n) for n in sequence[i].split('.')]
        next_para = [int(n) for n in sequence[i+1].split('.')]
        if next_para < current:
            violations.append((sequence[i], sequence[i+1]))
    return violations

# --- 5. Generate Report ---
def generate_report(ad_paras, jr_refs, dr_refs, covered_by_jr, covered_by_dr, covered_by_both, uncovered, jr_violations, dr_violations):
    total_covered = len(covered_by_jr) + len(covered_by_dr) + len(covered_by_both)
    coverage_percentage = (total_covered / len(ad_paras) * 100) if ad_paras else 0

    report = f"""# V9 AD Paragraph Coverage and Alignment Report

**Date:** November 2, 2025

## Summary

- **Total AD paragraphs:** {len(ad_paras)}
- **Covered by JR only:** {len(covered_by_jr)}
- **Covered by DR only:** {len(covered_by_dr)}
- **Covered by both JR and DR:** {len(covered_by_both)}
- **Total covered:** {total_covered}
- **Uncovered:** {len(uncovered)}
- **Coverage percentage:** {coverage_percentage:.1f}%

"""

    if uncovered:
        report += f"## Uncovered AD Paragraphs ({len(uncovered)})\n"
        for para in sorted(uncovered, key=lambda x: [int(n) for n in x.split('.')]):
            report += f"- AD {para}\n"

    report += "\n## Order Verification\n"
    report += "\n### JR Affidavit Order\n"
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
        
    return report

# --- Main Execution ---
def main():
    print("Starting v9 affidavit verification...")
    ad_paragraphs = get_ad_paragraphs(AD_REF_FILE)
    jr_references = get_references(JR_AFFIDAVIT_V9, "JR")
    dr_references = get_references(DR_AFFIDAVIT_V9, "DR")

    covered_jr, covered_dr, covered_both, uncovered = check_coverage(ad_paragraphs, jr_references, dr_references)
    
    jr_order_violations = check_order(JR_AFFIDAVIT_V9, "JR")
    dr_order_violations = check_order(DR_AFFIDAVIT_V9, "DR")

    report_content = generate_report(ad_paragraphs, jr_references, dr_references, covered_jr, covered_dr, covered_both, uncovered, jr_order_violations, dr_order_violations)

    OUTPUT_REPORT_FILE.write_text(report_content)
    print(f"✓ Verification complete. Report saved to {OUTPUT_REPORT_FILE}")

if __name__ == "__main__":
    main()


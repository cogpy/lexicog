#!/usr/bin/env python3
"""
Verify AD paragraph coverage in the v11 affidavits against the 132-paragraph structure.
"""
import re
from pathlib import Path

# --- Configuration ---
AD_REF_FILE = Path("/home/ubuntu/canima/AD_Paragraph_Order_Reference_132.txt")
JR_AFFIDAVIT_V11 = Path("/home/ubuntu/canima/affidavits_refined/Jacqueline_Answering_Affidavit_v11_FINAL.md")
DR_AFFIDAVIT_V11 = Path("/home/ubuntu/canima/affidavits_refined/Daniel_Answering_Affidavit_v11_FINAL.md")
OUTPUT_REPORT_FILE = Path("/home/ubuntu/canima/AD_COVERAGE_VERIFICATION_REPORT_V11.md")

# --- 1. Extract AD Paragraphs from Reference ---
def get_ad_paragraphs(ref_path):
    if not ref_path.exists():
        return []
    content = ref_path.read_text()
    ad_paragraphs = []
    for line in content.split('\n'):
        match = re.search(r'^\s*\d+\.\s+AD\s+([\d.]+)', line)
        if match:
            ad_para = match.group(1).strip()
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

# --- 4. Generate Report ---
def generate_report(ad_paras, jr_refs, dr_refs, covered_jr, covered_dr, covered_both, uncovered):
    total_covered = len(covered_jr) + len(covered_dr) + len(covered_both)
    coverage_percentage = (total_covered / len(ad_paras) * 100) if ad_paras else 0

    report = f"""# V11 AD Paragraph Coverage Verification Report (132-Paragraph Structure)

**Date:** November 2, 2025

## Summary

- **Total AD paragraphs (132-para structure):** {len(ad_paras)}
- **Covered by JR only:** {len(covered_jr)}
- **Covered by DR only:** {len(covered_dr)}
- **Covered by both JR and DR:** {len(covered_both)}
- **Total covered:** {total_covered}
- **Uncovered:** {len(uncovered)}
- **Coverage percentage:** {coverage_percentage:.1f}%

"""

    if uncovered:
        report += f"## ⚠ Uncovered AD Paragraphs ({len(uncovered)})\n\n"
        for para in sorted(uncovered, key=lambda x: [int(n) for n in x.split('.')]):
            report += f"- AD {para}\n"
    else:
        report += "## ✓ All AD Paragraphs Covered\n\n"

    report += "\n## Analysis\n\n"
    report += f"The v11 affidavits were enhanced with Jax's notes. "
    report += f"The current coverage is {coverage_percentage:.1f}% against the new 132-paragraph structure. "
    
    if uncovered:
        report += f"\n\nThe {len(uncovered)} uncovered paragraphs are new additions to the 132-paragraph structure "
        report += "that were not present in the original 100-paragraph reference. These need to be addressed "
        report += "in the next version of the affidavits.\n"
    
    return report

# --- Main Execution ---
def main():
    print("Starting v11 affidavit coverage verification...")
    ad_paragraphs = get_ad_paragraphs(AD_REF_FILE)
    jr_references = get_references(JR_AFFIDAVIT_V11, "JR")
    dr_references = get_references(DR_AFFIDAVIT_V11, "DR")

    covered_jr, covered_dr, covered_both, uncovered = check_coverage(ad_paragraphs, jr_references, dr_references)

    report_content = generate_report(ad_paragraphs, jr_references, dr_references, covered_jr, covered_dr, covered_both, uncovered)

    OUTPUT_REPORT_FILE.write_text(report_content)
    print(f"✓ Verification complete. Report saved to {OUTPUT_REPORT_FILE}")
    print(f"Coverage: {((len(covered_jr) + len(covered_dr) + len(covered_both)) / len(ad_paragraphs) * 100):.1f}%")

if __name__ == "__main__":
    main()


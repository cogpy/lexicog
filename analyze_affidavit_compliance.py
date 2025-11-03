#!/usr/bin/env python3
"""Analyze current Jax and Dan affidavits for compliance and gaps."""

import json
import re

def extract_response_numbers(file_path, prefix):
    """Extract all JR or DR response numbers from affidavit."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match JR X.Y or DR X.Y
    pattern = rf'\*\*{prefix}\s+(\d+(?:\.\d+)+)\*\*'
    matches = re.findall(pattern, content)
    
    return sorted(set(matches), key=lambda x: [int(p) for p in x.split('.')])

def load_ad_numbers():
    """Load all AD paragraph numbers."""
    with open('/home/ubuntu/canima/ad_paragraphs_complete.json', 'r') as f:
        paragraphs = json.load(f)
    
    return [p['number'] for p in paragraphs]

def check_ordering(responses, prefix):
    """Check if responses are in correct order."""
    violations = []
    
    for i in range(len(responses) - 1):
        current = [int(p) for p in responses[i].split('.')]
        next_resp = [int(p) for p in responses[i+1].split('.')]
        
        # Check if next is greater than current
        if next_resp <= current:
            violations.append({
                'current': responses[i],
                'next': responses[i+1],
                'position': i
            })
    
    return violations

def analyze_coverage(ad_numbers, jr_numbers, dr_numbers):
    """Analyze which AD paragraphs are covered by responses."""
    ad_set = set(ad_numbers)
    jr_set = set(jr_numbers)
    dr_set = set(dr_numbers)
    
    jr_missing = ad_set - jr_set
    dr_missing = ad_set - dr_set
    
    jr_extra = jr_set - ad_set
    dr_extra = dr_set - ad_set
    
    return {
        'jr_missing': sorted(jr_missing, key=lambda x: [int(p) for p in x.split('.')]),
        'dr_missing': sorted(dr_missing, key=lambda x: [int(p) for p in x.split('.')]),
        'jr_extra': sorted(jr_extra, key=lambda x: [int(p) for p in x.split('.')]),
        'dr_extra': sorted(dr_extra, key=lambda x: [int(p) for p in x.split('.')]),
        'jr_coverage': len(jr_set & ad_set) / len(ad_set) * 100,
        'dr_coverage': len(dr_set & ad_set) / len(ad_set) * 100
    }

def check_response_content(file_path, response_numbers, prefix):
    """Check if responses have actual content or just placeholders."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    placeholder_responses = []
    
    for resp_num in response_numbers:
        # Find the response section
        pattern = rf'\*\*{prefix}\s+{re.escape(resp_num)}\*\*\s+(.+?)(?=\*\*{prefix}|\Z)'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            resp_content = match.group(1).strip()
            # Check for placeholder text
            if '[RESPONSE REQUIRED]' in resp_content or len(resp_content) < 50:
                placeholder_responses.append(resp_num)
    
    return placeholder_responses

def generate_compliance_report():
    """Generate comprehensive compliance analysis report."""
    # Load data
    ad_numbers = load_ad_numbers()
    
    jr_file = '/home/ubuntu/canima/affidavits_refined/Jacqueline_Answering_Affidavit_v14_FINAL.md'
    dr_file = '/home/ubuntu/canima/affidavits_refined/Daniel_Answering_Affidavit_v14_FINAL.md'
    
    jr_numbers = extract_response_numbers(jr_file, 'JR')
    dr_numbers = extract_response_numbers(dr_file, 'DR')
    
    # Check ordering
    jr_order_violations = check_ordering(jr_numbers, 'JR')
    dr_order_violations = check_ordering(dr_numbers, 'DR')
    
    # Analyze coverage
    coverage = analyze_coverage(ad_numbers, jr_numbers, dr_numbers)
    
    # Check for placeholders
    jr_placeholders = check_response_content(jr_file, jr_numbers, 'JR')
    dr_placeholders = check_response_content(dr_file, dr_numbers, 'DR')
    
    # Generate report
    report = {
        'analysis_date': '2025-11-03',
        'total_ad_paragraphs': len(ad_numbers),
        'jacqueline_affidavit': {
            'total_responses': len(jr_numbers),
            'coverage_percentage': coverage['jr_coverage'],
            'missing_ad_paragraphs': coverage['jr_missing'],
            'extra_responses': coverage['jr_extra'],
            'ordering_violations': jr_order_violations,
            'placeholder_responses': jr_placeholders
        },
        'daniel_affidavit': {
            'total_responses': len(dr_numbers),
            'coverage_percentage': coverage['dr_coverage'],
            'missing_ad_paragraphs': coverage['dr_missing'],
            'extra_responses': coverage['dr_extra'],
            'ordering_violations': dr_order_violations,
            'placeholder_responses': dr_placeholders
        }
    }
    
    # Save JSON report
    with open('/home/ubuntu/canima/AFFIDAVIT_COMPLIANCE_ANALYSIS.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    # Generate markdown report
    md_lines = [
        "# Affidavit Compliance Analysis Report",
        "",
        f"**Analysis Date:** {report['analysis_date']}",
        f"**Total AD Paragraphs:** {report['total_ad_paragraphs']}",
        "",
        "## Jacqueline Faucitt (JR) Affidavit",
        "",
        f"- **Total Responses:** {report['jacqueline_affidavit']['total_responses']}",
        f"- **Coverage:** {report['jacqueline_affidavit']['coverage_percentage']:.1f}%",
        f"- **Missing AD Paragraphs:** {len(report['jacqueline_affidavit']['missing_ad_paragraphs'])}",
        f"- **Ordering Violations:** {len(report['jacqueline_affidavit']['ordering_violations'])}",
        f"- **Placeholder Responses:** {len(report['jacqueline_affidavit']['placeholder_responses'])}",
        ""
    ]
    
    if report['jacqueline_affidavit']['missing_ad_paragraphs']:
        md_lines.append("### Missing AD Paragraphs (JR)")
        md_lines.append("")
        for ad_num in report['jacqueline_affidavit']['missing_ad_paragraphs'][:20]:
            md_lines.append(f"- AD {ad_num}")
        if len(report['jacqueline_affidavit']['missing_ad_paragraphs']) > 20:
            md_lines.append(f"- ... and {len(report['jacqueline_affidavit']['missing_ad_paragraphs']) - 20} more")
        md_lines.append("")
    
    if report['jacqueline_affidavit']['ordering_violations']:
        md_lines.append("### Ordering Violations (JR)")
        md_lines.append("")
        for violation in report['jacqueline_affidavit']['ordering_violations']:
            md_lines.append(f"- JR {violation['current']} followed by JR {violation['next']} (out of order)")
        md_lines.append("")
    
    md_lines.extend([
        "## Daniel Faucitt (DR) Affidavit",
        "",
        f"- **Total Responses:** {report['daniel_affidavit']['total_responses']}",
        f"- **Coverage:** {report['daniel_affidavit']['coverage_percentage']:.1f}%",
        f"- **Missing AD Paragraphs:** {len(report['daniel_affidavit']['missing_ad_paragraphs'])}",
        f"- **Ordering Violations:** {len(report['daniel_affidavit']['ordering_violations'])}",
        f"- **Placeholder Responses:** {len(report['daniel_affidavit']['placeholder_responses'])}",
        ""
    ])
    
    if report['daniel_affidavit']['missing_ad_paragraphs']:
        md_lines.append("### Missing AD Paragraphs (DR)")
        md_lines.append("")
        for ad_num in report['daniel_affidavit']['missing_ad_paragraphs'][:20]:
            md_lines.append(f"- AD {ad_num}")
        if len(report['daniel_affidavit']['missing_ad_paragraphs']) > 20:
            md_lines.append(f"- ... and {len(report['daniel_affidavit']['missing_ad_paragraphs']) - 20} more")
        md_lines.append("")
    
    if report['daniel_affidavit']['ordering_violations']:
        md_lines.append("### Ordering Violations (DR)")
        md_lines.append("")
        for violation in report['daniel_affidavit']['ordering_violations']:
            md_lines.append(f"- DR {violation['current']} followed by DR {violation['next']} (out of order)")
        md_lines.append("")
    
    md_lines.extend([
        "## Summary of Issues",
        "",
        "### Critical Issues",
        ""
    ])
    
    critical_issues = []
    if len(report['jacqueline_affidavit']['missing_ad_paragraphs']) > 0:
        critical_issues.append(f"- JR affidavit missing {len(report['jacqueline_affidavit']['missing_ad_paragraphs'])} AD paragraph responses")
    if len(report['daniel_affidavit']['missing_ad_paragraphs']) > 0:
        critical_issues.append(f"- DR affidavit missing {len(report['daniel_affidavit']['missing_ad_paragraphs'])} AD paragraph responses")
    if len(report['jacqueline_affidavit']['placeholder_responses']) > 50:
        critical_issues.append(f"- JR affidavit has {len(report['jacqueline_affidavit']['placeholder_responses'])} placeholder responses")
    if len(report['daniel_affidavit']['placeholder_responses']) > 50:
        critical_issues.append(f"- DR affidavit has {len(report['daniel_affidavit']['placeholder_responses'])} placeholder responses")
    
    md_lines.extend(critical_issues)
    md_lines.append("")
    
    # Save markdown report
    with open('/home/ubuntu/canima/AFFIDAVIT_COMPLIANCE_ANALYSIS.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))
    
    print("✓ Affidavit compliance analysis completed")
    print(f"\nJacqueline (JR) Affidavit:")
    print(f"  - Coverage: {report['jacqueline_affidavit']['coverage_percentage']:.1f}%")
    print(f"  - Missing: {len(report['jacqueline_affidavit']['missing_ad_paragraphs'])} AD paragraphs")
    print(f"  - Ordering violations: {len(report['jacqueline_affidavit']['ordering_violations'])}")
    print(f"  - Placeholders: {len(report['jacqueline_affidavit']['placeholder_responses'])}")
    
    print(f"\nDaniel (DR) Affidavit:")
    print(f"  - Coverage: {report['daniel_affidavit']['coverage_percentage']:.1f}%")
    print(f"  - Missing: {len(report['daniel_affidavit']['missing_ad_paragraphs'])} AD paragraphs")
    print(f"  - Ordering violations: {len(report['daniel_affidavit']['ordering_violations'])}")
    print(f"  - Placeholders: {len(report['daniel_affidavit']['placeholder_responses'])}")
    
    print("\nFiles created:")
    print("  - AFFIDAVIT_COMPLIANCE_ANALYSIS.json")
    print("  - AFFIDAVIT_COMPLIANCE_ANALYSIS.md")

if __name__ == '__main__':
    generate_compliance_report()

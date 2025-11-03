#!/usr/bin/env python3
"""Map AD paragraph structure and categorize by allegation severity."""

import json
import re

def categorize_severity(para_num, content):
    """Categorize paragraph by severity (green=neutral, yellow=concern, red=serious)."""
    content_lower = content.lower()
    
    # Serious allegations (RED)
    serious_keywords = [
        'fraud', 'delinquency', 'gross negligence', 'misappropriation',
        'unauthorized', 'irregular', 'unexplained', 'refused',
        'interfered', 'sabotage', 'malicious', 'criminal'
    ]
    
    # Concerns (YELLOW)
    concern_keywords = [
        'discrepancies', 'erratic', 'could not explain', 'problems',
        'halted', 'superior position', 'declined'
    ]
    
    # Neutral/factual (GREEN) - typically identification, jurisdiction, etc.
    neutral_sections = ['1.', '2.', '3.', '4.', '5.', '6.', '21']
    
    # Check section
    section = para_num.split('.')[0]
    
    if any(kw in content_lower for kw in serious_keywords):
        return 'red', 'serious_allegation'
    elif any(kw in content_lower for kw in concern_keywords):
        return 'yellow', 'concern'
    elif section in neutral_sections:
        return 'green', 'neutral_factual'
    else:
        return 'yellow', 'general_claim'

def extract_section_info(para_num):
    """Extract section information from paragraph number."""
    parts = para_num.split('.')
    section_map = {
        '1': 'Introduction',
        '2': 'Applicant',
        '3': 'Identification of Respondents',
        '4': 'Jurisdiction',
        '5': 'Locus Standi',
        '6': 'Relationships',
        '7': 'Discovery of Financial Irregularities',
        '8': 'IT Expenses Analysis',
        '9': 'Bantjies Debt',
        '10': 'Grounds for Delinquency Declaration',
        '11': 'Grounds for Interdict',
        '12': 'Grounds for Preservation Orders',
        '13': 'Requirements for Interdict',
        '14': 'Requirements for Preservation Orders',
        '15': 'Costs',
        '16': 'Urgency',
        '17': 'Ex Parte Application',
        '21': 'Oath Declaration'
    }
    
    section = parts[0]
    return {
        'section_num': section,
        'section_title': section_map.get(section, f'Section {section}'),
        'depth': len(parts)
    }

def main():
    # Load extracted paragraphs
    with open('/home/ubuntu/canima/ad_paragraphs_complete.json', 'r') as f:
        paragraphs = json.load(f)
    
    # Map structure
    mapped = []
    for para in paragraphs:
        section_info = extract_section_info(para['number'])
        color, category = categorize_severity(para['number'], para['content'])
        
        mapped.append({
            'ad_number': para['number'],
            'section_num': section_info['section_num'],
            'section_title': section_info['section_title'],
            'depth': section_info['depth'],
            'content': para['content'],
            'severity_color': color,
            'category': category,
            'content_preview': para['content'][:100] + '...' if len(para['content']) > 100 else para['content']
        })
    
    # Save mapped structure
    with open('/home/ubuntu/canima/ad_structure_mapped.json', 'w', encoding='utf-8') as f:
        json.dump(mapped, f, indent=2, ensure_ascii=False)
    
    # Generate summary report
    report_lines = [
        "# AD Paragraph Structure and Severity Mapping",
        "",
        f"**Total AD Paragraphs:** {len(mapped)}",
        "",
        "## Severity Distribution",
        ""
    ]
    
    # Count by severity
    severity_counts = {}
    for item in mapped:
        color = item['severity_color']
        severity_counts[color] = severity_counts.get(color, 0) + 1
    
    report_lines.append(f"- 🟢 **Green (Neutral/Factual):** {severity_counts.get('green', 0)}")
    report_lines.append(f"- 🟡 **Yellow (Concern/Claim):** {severity_counts.get('yellow', 0)}")
    report_lines.append(f"- 🔴 **Red (Serious Allegation):** {severity_counts.get('red', 0)}")
    report_lines.append("")
    
    # Group by section
    report_lines.append("## Section Breakdown")
    report_lines.append("")
    
    current_section = None
    for item in mapped:
        if item['section_num'] != current_section:
            current_section = item['section_num']
            report_lines.append(f"### Section {current_section}: {item['section_title']}")
            report_lines.append("")
        
        # Color indicator
        color_emoji = {'green': '🟢', 'yellow': '🟡', 'red': '🔴'}[item['severity_color']]
        report_lines.append(f"{color_emoji} **AD {item['ad_number']}** - {item['content_preview']}")
        report_lines.append("")
    
    # Save report
    with open('/home/ubuntu/canima/AD_STRUCTURE_SEVERITY_MAP.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print(f"✓ Mapped {len(mapped)} AD paragraphs")
    print(f"✓ Severity distribution: Green={severity_counts.get('green', 0)}, Yellow={severity_counts.get('yellow', 0)}, Red={severity_counts.get('red', 0)}")
    print("\nFiles created:")
    print("  - ad_structure_mapped.json")
    print("  - AD_STRUCTURE_SEVERITY_MAP.md")

if __name__ == '__main__':
    main()

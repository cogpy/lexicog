#!/usr/bin/env python3
"""Comprehensive legal analysis integrating entities, relations, events, and timelines."""

import json
from datetime import datetime

def load_existing_data():
    """Load existing analysis data."""
    data = {}
    
    # Load legal aspects
    with open('/home/ubuntu/canima/analysis/legal_aspects.json', 'r') as f:
        data['legal_aspects'] = json.load(f)
    
    # Load entities
    with open('/home/ubuntu/canima/analysis/entities.json', 'r') as f:
        data['entities'] = json.load(f)
    
    # Load relations
    with open('/home/ubuntu/canima/analysis/relations.json', 'r') as f:
        data['relations'] = json.load(f)
    
    # Load timeline
    with open('/home/ubuntu/canima/analysis/timeline.json', 'r') as f:
        data['timeline'] = json.load(f)
    
    # Load AD structure
    with open('/home/ubuntu/canima/ad_structure_mapped.json', 'r') as f:
        data['ad_structure'] = json.load(f)
    
    return data

def identify_relevant_laws():
    """Identify relevant South African laws and sections."""
    return {
        "Companies Act 71 of 2008": {
            "sections": {
                "Section 162(2)": "Locus standi for delinquency applications",
                "Section 162(5)(c)(ii)": "Gross abuse of position of director",
                "Section 162(5)(c)(iii)": "Intentional or grossly negligent infliction of harm",
                "Section 162(5)(c)(iv)(bb)": "Party to act/omission despite knowledge of recklessness",
                "Section 76": "Standards of directors' conduct",
                "Section 77": "Liability of directors and prescribed officers"
            }
        },
        "Trust Property Control Act 57 of 1988": {
            "sections": {
                "Section 9(1)": "Trustee duty to act in beneficiaries' interests",
                "Section 9(2)": "Trustee duty of care and diligence",
                "Section 12": "Removal of trustees",
                "Section 16": "Accountability and disclosure requirements"
            }
        },
        "Prevention and Combating of Corrupt Activities Act 12 of 2004": {
            "sections": {
                "Section 4": "General offence of corruption",
                "Section 34": "Duty to report corrupt transactions"
            }
        },
        "Financial Intelligence Centre Act 38 of 2001": {
            "sections": {
                "Section 29": "Reporting of suspicious transactions"
            }
        }
    }

def map_ad_to_legal_provisions(ad_structure):
    """Map AD paragraphs to relevant legal provisions."""
    mappings = []
    
    for ad in ad_structure:
        ad_num = ad['ad_number']
        section = ad['section_num']
        content_lower = ad['content'].lower()
        
        relevant_laws = []
        
        # Section 7: Financial irregularities
        if section == '7':
            if 'unexplained' in content_lower or 'irregular' in content_lower:
                relevant_laws.append("Companies Act s76 - Director's duty of care")
                relevant_laws.append("Companies Act s77 - Liability for breach")
        
        # Section 8: IT expenses
        if section == '8':
            relevant_laws.append("Companies Act s76 - Proper financial management")
        
        # Section 9: Bantjies debt
        if section == '9':
            relevant_laws.append("Trust Property Control Act s9(1) - Conflict of interest")
            relevant_laws.append("Companies Act s75 - Personal financial interest")
        
        # Section 10: Delinquency
        if section == '10':
            if '162(5)(c)' in ad['content']:
                relevant_laws.append("Companies Act s162(5)(c) - Delinquency grounds")
        
        # Section 11: Interdict grounds
        if section == '11':
            relevant_laws.append("Common law - Interdict requirements")
            relevant_laws.append("Companies Act s162 - Protection of company")
        
        if relevant_laws:
            mappings.append({
                'ad_number': ad_num,
                'section_title': ad['section_title'],
                'relevant_laws': relevant_laws
            })
    
    return mappings

def analyze_conflicts_of_interest(entities, relations):
    """Analyze conflicts of interest among parties."""
    conflicts = []
    
    # Bantjies conflict
    conflicts.append({
        'party': 'Danie Bantjies',
        'roles': [
            'Trustee of Faucitt Family Trust (undisclosed)',
            'Accountant for RegimA companies',
            'Debtor to Peter Faucitt (R18.685M)',
            'Company Controller',
            'Commissioner of Oaths for Peter\'s affidavit'
        ],
        'conflict_nature': 'Irreconcilable multiple roles with competing interests',
        'legal_breach': 'Trust Property Control Act s9(1) - Duty to act in beneficiaries\' interests',
        'impact': 'Unable to impartially investigate fraud reported by beneficiary Daniel',
        'evidence': 'Dismissed audit request on 10 June 2025 claiming "going on holiday"'
    })
    
    # Peter conflict
    conflicts.append({
        'party': 'Peter Faucitt',
        'roles': [
            'Trustee of Faucitt Family Trust',
            'Founder with special powers',
            'Applicant seeking interdict against beneficiaries'
        ],
        'conflict_nature': 'Trustee attacking beneficiaries of own trust',
        'legal_breach': 'Trust Property Control Act s9(1) - Fiduciary duty to beneficiaries',
        'impact': 'Using trust-owned companies and assets to attack beneficiaries',
        'evidence': 'Interdict filed 24 Sep 2025 against Jax (co-trustee/beneficiary) and Dan (beneficiary)'
    })
    
    # Rynette control
    conflicts.append({
        'party': 'Rynette Farrar',
        'roles': [
            'Controller of accounting system (Sage)',
            'Controller of pete@regima.com email',
            'Mother of Adderory owner (supplier to RegimA)'
        ],
        'conflict_nature': 'Unauthorized control with undisclosed related party transactions',
        'legal_breach': 'Companies Act s76 - Unauthorized exercise of powers',
        'impact': 'Two years unallocated expenses, R5.4M stock adjustment fraud',
        'evidence': 'SARS audit email claiming Bantjies instructed huge payments'
    })
    
    return conflicts

def generate_comprehensive_report(data):
    """Generate comprehensive legal analysis report."""
    laws = identify_relevant_laws()
    ad_law_mappings = map_ad_to_legal_provisions(data['ad_structure'])
    conflicts = analyze_conflicts_of_interest(data['entities'], data['relations'])
    
    report = {
        'generated': datetime.now().isoformat(),
        'case_number': '2025-137857',
        'court': 'High Court of South Africa, Gauteng Division, Pretoria',
        'summary': {
            'total_ad_paragraphs': len(data['ad_structure']),
            'serious_allegations': len([ad for ad in data['ad_structure'] if ad['severity_color'] == 'red']),
            'entities_identified': len(data['entities']),
            'timeline_events': len(data['timeline']),
            'conflicts_of_interest': len(conflicts)
        },
        'relevant_laws': laws,
        'ad_legal_mappings': ad_law_mappings,
        'conflicts_of_interest': conflicts,
        'legal_aspects': data['legal_aspects'],
        'timeline': data['timeline'],
        'entities': data['entities'],
        'relations': data['relations']
    }
    
    # Save comprehensive report
    with open('/home/ubuntu/canima/LEGAL_ANALYSIS_COMPREHENSIVE.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    # Generate markdown report
    md_lines = [
        "# Comprehensive Legal Analysis Report",
        "",
        f"**Case No:** {report['case_number']}",
        f"**Court:** {report['court']}",
        f"**Generated:** {report['generated']}",
        "",
        "## Executive Summary",
        "",
        f"- **Total AD Paragraphs:** {report['summary']['total_ad_paragraphs']}",
        f"- **Serious Allegations:** {report['summary']['serious_allegations']}",
        f"- **Entities Identified:** {report['summary']['entities_identified']}",
        f"- **Timeline Events:** {report['summary']['timeline_events']}",
        f"- **Conflicts of Interest:** {report['summary']['conflicts_of_interest']}",
        "",
        "## Relevant Legal Framework",
        ""
    ]
    
    for act, details in laws.items():
        md_lines.append(f"### {act}")
        md_lines.append("")
        for section, description in details['sections'].items():
            md_lines.append(f"- **{section}:** {description}")
        md_lines.append("")
    
    md_lines.extend([
        "## Conflicts of Interest Analysis",
        ""
    ])
    
    for conflict in conflicts:
        md_lines.append(f"### {conflict['party']}")
        md_lines.append("")
        md_lines.append("**Roles:**")
        for role in conflict['roles']:
            md_lines.append(f"- {role}")
        md_lines.append("")
        md_lines.append(f"**Conflict Nature:** {conflict['conflict_nature']}")
        md_lines.append("")
        md_lines.append(f"**Legal Breach:** {conflict['legal_breach']}")
        md_lines.append("")
        md_lines.append(f"**Impact:** {conflict['impact']}")
        md_lines.append("")
        md_lines.append(f"**Evidence:** {conflict['evidence']}")
        md_lines.append("")
    
    md_lines.extend([
        "## Material Non-Disclosures",
        ""
    ])
    
    for nondisclosure in data['legal_aspects']['material_non_disclosures']:
        md_lines.append(f"### {nondisclosure['what']}")
        md_lines.append("")
        md_lines.append(f"**Status:** {nondisclosure['status']}")
        md_lines.append(f"**Impact:** {nondisclosure['impact']}")
        md_lines.append("")
    
    # Save markdown report
    with open('/home/ubuntu/canima/LEGAL_ANALYSIS_COMPREHENSIVE.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))
    
    print("✓ Comprehensive legal analysis completed")
    print(f"  - {report['summary']['total_ad_paragraphs']} AD paragraphs analyzed")
    print(f"  - {report['summary']['serious_allegations']} serious allegations identified")
    print(f"  - {len(conflicts)} conflicts of interest documented")
    print(f"  - {len(ad_law_mappings)} AD-law mappings created")
    print("\nFiles created:")
    print("  - LEGAL_ANALYSIS_COMPREHENSIVE.json")
    print("  - LEGAL_ANALYSIS_COMPREHENSIVE.md")

def main():
    data = load_existing_data()
    generate_comprehensive_report(data)

if __name__ == '__main__':
    main()

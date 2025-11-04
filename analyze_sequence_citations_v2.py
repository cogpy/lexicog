#!/usr/bin/env python3
"""
Analyze AD paragraph coverage and citation quality - Version 2
"""
import re
import json
from pathlib import Path

def extract_ad_sequence(file_path):
    """Extract AD paragraphs in their original sequence"""
    ad_sequence = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(r'\s*\d+\.\s+AD\s+([\d.]+)', line)
            if match:
                ad_num = match.group(1).strip()
                # Normalize "AD 2025" to skip it
                if ad_num != "2025":
                    ad_sequence.append(ad_num)
    return ad_sequence

def extract_response_sequence(file_path, prefix='JR'):
    """Extract response paragraphs - handle both base and sub-numbered responses"""
    responses = []
    base_responses = set()
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        pattern = rf'\*\*{prefix}\s+([\d.]+)\*\*'
        for match in re.finditer(pattern, content):
            full_num = match.group(1).strip()
            responses.append(full_num)
            # Extract base number (e.g., "7.5" from "7.5.1")
            base_num = '.'.join(full_num.split('.')[:2])
            base_responses.add(base_num)
    return responses, base_responses

def analyze_citation_quality(file_path, prefix='JR'):
    """Analyze citation quality in responses"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all response blocks - more flexible pattern
    pattern = rf'\*\*{prefix}\s+([\d.]+)\*\*\s*(.*?)(?=\*\*(?:{prefix}|JR|DR)|\Z)'
    matches = re.finditer(pattern, content, re.DOTALL)
    
    citation_analysis = []
    for match in matches:
        para_num = match.group(1)
        para_text = match.group(2).strip()
        
        # Check for citations
        has_annexure = bool(re.search(r'\[(?:JR|DR|PF)-[\d.]+', para_text))
        has_legal_ref = bool(re.search(r'(?:Section|Act|s\.|ss\.)\s+\d+', para_text))
        
        # Check for placeholder text
        has_placeholder = bool(re.search(r'\[Add specific response|Add annexure citation|if required\]', para_text))
        
        # Check content length
        word_count = len(para_text.split())
        
        citation_analysis.append({
            'paragraph': para_num,
            'has_annexure_citation': has_annexure,
            'has_legal_reference': has_legal_ref,
            'has_placeholder': has_placeholder,
            'word_count': word_count,
            'is_substantive': word_count > 15 and not has_placeholder
        })
    
    return citation_analysis

def main():
    # Paths
    ad_ref_path = Path('/home/ubuntu/canima/AD_Paragraph_Order_Reference_132.txt')
    jax_path = Path('/home/ubuntu/canima/affidavits_refined/Jacqueline_Answering_Affidavit_v15_CITED.md')
    dan_path = Path('/home/ubuntu/canima/affidavits_refined/Daniel_Answering_Affidavit_v9_DR.md')
    
    # Extract sequences
    ad_sequence = extract_ad_sequence(ad_ref_path)
    jr_responses, jr_base = extract_response_sequence(jax_path, 'JR')
    dr_responses, dr_base = extract_response_sequence(dan_path, 'DR')
    
    print("="*80)
    print("AD PARAGRAPH COVERAGE ANALYSIS")
    print("="*80)
    print(f"\nTotal AD Paragraphs: {len(ad_sequence)}")
    print(f"JR Base Responses: {len(jr_base)}")
    print(f"JR Total Responses (including sub-numbered): {len(jr_responses)}")
    print(f"DR Base Responses: {len(dr_base)}")
    print(f"DR Total Responses (including sub-numbered): {len(dr_responses)}")
    
    # Find missing base responses
    ad_set = set(ad_sequence)
    missing_jr = ad_set - jr_base
    missing_dr = ad_set - dr_base
    
    print(f"\n" + "="*80)
    print("MISSING RESPONSES")
    print("="*80)
    print(f"\nMissing JR Responses: {len(missing_jr)}")
    if missing_jr:
        for ad_num in sorted(missing_jr, key=lambda x: [int(n) for n in x.split('.')]):
            print(f"  AD {ad_num}")
    
    print(f"\nMissing DR Responses: {len(missing_dr)}")
    if missing_dr:
        for ad_num in sorted(missing_dr, key=lambda x: [int(n) for n in x.split('.')]):
            print(f"  AD {ad_num}")
    
    print("\n" + "="*80)
    print("CITATION QUALITY ANALYSIS")
    print("="*80)
    
    # Analyze JR citations
    jr_citations = analyze_citation_quality(jax_path, 'JR')
    if len(jr_citations) > 0:
        jr_with_annexures = sum(1 for c in jr_citations if c['has_annexure_citation'])
        jr_with_legal = sum(1 for c in jr_citations if c['has_legal_reference'])
        jr_with_placeholders = sum(1 for c in jr_citations if c['has_placeholder'])
        jr_substantive = sum(1 for c in jr_citations if c['is_substantive'])
        
        print(f"\nJR Citation Analysis:")
        print(f"  Total responses: {len(jr_citations)}")
        print(f"  With annexure citations: {jr_with_annexures} ({jr_with_annexures/len(jr_citations)*100:.1f}%)")
        print(f"  With legal references: {jr_with_legal} ({jr_with_legal/len(jr_citations)*100:.1f}%)")
        print(f"  With placeholders: {jr_with_placeholders} ({jr_with_placeholders/len(jr_citations)*100:.1f}%)")
        print(f"  Substantive responses: {jr_substantive} ({jr_substantive/len(jr_citations)*100:.1f}%)")
    
    # Analyze DR citations
    dr_citations = analyze_citation_quality(dan_path, 'DR')
    if len(dr_citations) > 0:
        dr_with_annexures = sum(1 for c in dr_citations if c['has_annexure_citation'])
        dr_with_legal = sum(1 for c in dr_citations if c['has_legal_reference'])
        dr_with_placeholders = sum(1 for c in dr_citations if c['has_placeholder'])
        dr_substantive = sum(1 for c in dr_citations if c['is_substantive'])
        
        print(f"\nDR Citation Analysis:")
        print(f"  Total responses: {len(dr_citations)}")
        print(f"  With annexure citations: {dr_with_annexures} ({dr_with_annexures/len(dr_citations)*100:.1f}%)")
        print(f"  With legal references: {dr_with_legal} ({dr_with_legal/len(dr_citations)*100:.1f}%)")
        print(f"  With placeholders: {dr_with_placeholders} ({dr_with_placeholders/len(dr_citations)*100:.1f}%)")
        print(f"  Substantive responses: {dr_substantive} ({dr_substantive/len(dr_citations)*100:.1f}%)")
    
    # Save detailed results
    results = {
        'ad_paragraph_count': len(ad_sequence),
        'jr_base_count': len(jr_base),
        'jr_total_count': len(jr_responses),
        'dr_base_count': len(dr_base),
        'dr_total_count': len(dr_responses),
        'missing_jr': sorted(list(missing_jr), key=lambda x: [int(n) for n in x.split('.')]),
        'missing_dr': sorted(list(missing_dr), key=lambda x: [int(n) for n in x.split('.')]),
        'jr_coverage_percent': round((len(jr_base) / len(ad_sequence)) * 100, 2),
        'dr_coverage_percent': round((len(dr_base) / len(ad_sequence)) * 100, 2),
        'jr_citation_analysis': jr_citations if len(jr_citations) > 0 else [],
        'dr_citation_analysis': dr_citations if len(dr_citations) > 0 else []
    }
    
    with open('/home/ubuntu/canima/COMPREHENSIVE_ANALYSIS.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "="*80)
    print(f"\nJR Coverage: {results['jr_coverage_percent']}%")
    print(f"DR Coverage: {results['dr_coverage_percent']}%")
    print("\nDetailed results saved to COMPREHENSIVE_ANALYSIS.json")

if __name__ == '__main__':
    main()

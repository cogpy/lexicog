#!/usr/bin/env python3
"""
Analyze the sequence order and citation quality of responses
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
                ad_sequence.append(match.group(1).strip())
    return ad_sequence

def extract_response_sequence(file_path, prefix='JR'):
    """Extract response paragraphs in their document sequence"""
    responses = []
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        pattern = rf'\*\*{prefix}\s+([\d.]+)\*\*'
        for match in re.finditer(pattern, content):
            responses.append(match.group(1).strip())
    return responses

def check_sequence_order(ad_sequence, response_sequence):
    """Check if responses follow AD paragraph order"""
    issues = []
    
    # Create position map for AD paragraphs
    ad_positions = {ad: idx for idx, ad in enumerate(ad_sequence)}
    
    # Check response order
    prev_position = -1
    for idx, resp_num in enumerate(response_sequence):
        if resp_num in ad_positions:
            curr_position = ad_positions[resp_num]
            if curr_position < prev_position:
                issues.append({
                    'response_index': idx,
                    'paragraph': resp_num,
                    'issue': 'Out of sequence',
                    'expected_position': curr_position,
                    'actual_position': idx
                })
            prev_position = curr_position
    
    return issues

def analyze_citation_quality(file_path, prefix='JR'):
    """Analyze citation quality in responses"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all response blocks
    pattern = rf'\*\*{prefix}\s+([\d.]+)\*\*\s*\n\n(.*?)(?=\*\*{prefix}|\Z)'
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
            'is_substantive': word_count > 20 and not has_placeholder
        })
    
    return citation_analysis

def main():
    # Paths
    ad_ref_path = Path('/home/ubuntu/canima/AD_Paragraph_Order_Reference_132.txt')
    jax_path = Path('/home/ubuntu/canima/affidavits_refined/Jacqueline_Answering_Affidavit_v15_CITED.md')
    dan_path = Path('/home/ubuntu/canima/affidavits_refined/Daniel_Answering_Affidavit_v9_DR.md')
    
    # Extract sequences
    ad_sequence = extract_ad_sequence(ad_ref_path)
    jr_sequence = extract_response_sequence(jax_path, 'JR')
    dr_sequence = extract_response_sequence(dan_path, 'DR')
    
    print("SEQUENCE ORDER ANALYSIS")
    print("="*80)
    
    # Check JR sequence
    jr_issues = check_sequence_order(ad_sequence, jr_sequence)
    print(f"\nJR Sequence Issues: {len(jr_issues)}")
    if jr_issues:
        for issue in jr_issues[:10]:  # Show first 10
            print(f"  {issue['paragraph']}: {issue['issue']}")
    
    # Check DR sequence
    dr_issues = check_sequence_order(ad_sequence, dr_sequence)
    print(f"\nDR Sequence Issues: {len(dr_issues)}")
    if dr_issues:
        for issue in dr_issues[:10]:  # Show first 10
            print(f"  {issue['paragraph']}: {issue['issue']}")
    
    print("\n" + "="*80)
    print("\nCITATION QUALITY ANALYSIS")
    print("="*80)
    
    # Analyze JR citations
    jr_citations = analyze_citation_quality(jax_path, 'JR')
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
        'jr_sequence_issues': jr_issues,
        'dr_sequence_issues': dr_issues,
        'jr_citation_analysis': jr_citations,
        'dr_citation_analysis': dr_citations,
        'summary': {
            'jr': {
                'sequence_issues': len(jr_issues),
                'with_annexures': jr_with_annexures,
                'with_legal_refs': jr_with_legal,
                'with_placeholders': jr_with_placeholders,
                'substantive': jr_substantive
            },
            'dr': {
                'sequence_issues': len(dr_issues),
                'with_annexures': dr_with_annexures,
                'with_legal_refs': dr_with_legal,
                'with_placeholders': dr_with_placeholders,
                'substantive': dr_substantive
            }
        }
    }
    
    with open('/home/ubuntu/canima/SEQUENCE_CITATION_ANALYSIS.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "="*80)
    print("\nDetailed results saved to SEQUENCE_CITATION_ANALYSIS.json")

if __name__ == '__main__':
    main()

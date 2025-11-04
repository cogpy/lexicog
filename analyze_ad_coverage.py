#!/usr/bin/env python3
"""
Analyze AD paragraph coverage in Jacqueline and Daniel's affidavits
"""
import re
import json
from pathlib import Path

def extract_ad_paragraphs(file_path):
    """Extract all AD paragraph references from the reference file"""
    ad_paragraphs = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # Match lines like "  1. AD 1.1 - ..."
            match = re.match(r'\s*\d+\.\s+(AD\s+[\d.]+)', line)
            if match:
                ad_num = match.group(1).strip()
                ad_paragraphs.append(ad_num)
    return ad_paragraphs

def extract_jr_responses(file_path):
    """Extract all JR paragraph references from Jacqueline's affidavit"""
    jr_responses = []
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # Match **JR X.Y** or **JR X.Y.Z**
        matches = re.findall(r'\*\*JR\s+([\d.]+)\*\*', content)
        jr_responses = [f"JR {m}" for m in matches]
    return jr_responses

def extract_dr_responses(file_path):
    """Extract all DR paragraph references from Daniel's affidavit"""
    dr_responses = []
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # Match **DR X.Y** or **DR X.Y.Z**
        matches = re.findall(r'\*\*DR\s+([\d.]+)\*\*', content)
        dr_responses = [f"DR {m}" for m in matches]
    return dr_responses

def normalize_ad_number(ad_str):
    """Normalize AD number for comparison (e.g., 'AD 1.1' -> '1.1')"""
    return ad_str.replace('AD ', '').strip()

def normalize_response_number(resp_str):
    """Normalize response number for comparison (e.g., 'JR 1.1' -> '1.1')"""
    return resp_str.replace('JR ', '').replace('DR ', '').strip()

def main():
    # Paths
    ad_ref_path = Path('/home/ubuntu/canima/AD_Paragraph_Order_Reference_132.txt')
    jax_path = Path('/home/ubuntu/canima/affidavits_refined/Jacqueline_Answering_Affidavit_v15_CITED.md')
    dan_path = Path('/home/ubuntu/canima/affidavits_refined/Daniel_Answering_Affidavit_v9_DR.md')
    
    # Extract data
    ad_paragraphs = extract_ad_paragraphs(ad_ref_path)
    jr_responses = extract_jr_responses(jax_path)
    dr_responses = extract_dr_responses(dan_path)
    
    print(f"Total AD Paragraphs: {len(ad_paragraphs)}")
    print(f"Total JR Responses: {len(jr_responses)}")
    print(f"Total DR Responses: {len(dr_responses)}")
    print("\n" + "="*80 + "\n")
    
    # Normalize for comparison
    ad_nums = set([normalize_ad_number(ad) for ad in ad_paragraphs])
    jr_nums = set([normalize_response_number(jr) for jr in jr_responses])
    dr_nums = set([normalize_response_number(dr) for dr in dr_responses])
    
    # Find missing responses
    missing_jr = ad_nums - jr_nums
    missing_dr = ad_nums - dr_nums
    
    print("MISSING JR RESPONSES:")
    print(f"Count: {len(missing_jr)}")
    if missing_jr:
        for ad_num in sorted(missing_jr, key=lambda x: [int(n) for n in x.split('.')]):
            print(f"  AD {ad_num}")
    print("\n" + "="*80 + "\n")
    
    print("MISSING DR RESPONSES:")
    print(f"Count: {len(missing_dr)}")
    if missing_dr:
        for ad_num in sorted(missing_dr, key=lambda x: [int(n) for n in x.split('.')]):
            print(f"  AD {ad_num}")
    print("\n" + "="*80 + "\n")
    
    # Save results
    results = {
        'total_ad_paragraphs': len(ad_paragraphs),
        'total_jr_responses': len(jr_responses),
        'total_dr_responses': len(dr_responses),
        'missing_jr': sorted(list(missing_jr), key=lambda x: [int(n) for n in x.split('.')]),
        'missing_dr': sorted(list(missing_dr), key=lambda x: [int(n) for n in x.split('.')]),
        'jr_coverage_percent': round((len(jr_nums) / len(ad_nums)) * 100, 2),
        'dr_coverage_percent': round((len(dr_nums) / len(ad_nums)) * 100, 2)
    }
    
    with open('/home/ubuntu/canima/AD_COVERAGE_ANALYSIS.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"JR Coverage: {results['jr_coverage_percent']}%")
    print(f"DR Coverage: {results['dr_coverage_percent']}%")
    print("\nResults saved to AD_COVERAGE_ANALYSIS.json")

if __name__ == '__main__':
    main()

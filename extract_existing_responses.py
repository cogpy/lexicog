#!/usr/bin/env python3
"""
Extract existing JR and DR responses from current affidavits and map to AD paragraphs.
"""
import re
from pathlib import Path
from collections import OrderedDict
import json

def extract_responses(file_path, prefix):
    """Extract all responses from an affidavit file"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    responses = OrderedDict()
    
    # Pattern to match response blocks like **JR 7.13** or **DR 3.4.2**
    # Capture everything until the next response or major section
    pattern = rf'\*\*{prefix}\s+([\d.]+)\*\*\s*\n(.*?)(?=\n\*\*{prefix}\s+[\d.]+\*\*|\n##\s+[^*]|$)'
    
    matches = re.finditer(pattern, content, re.DOTALL)
    
    for match in matches:
        para_num = match.group(1)
        full_text = match.group(2).strip()
        responses[para_num] = full_text
    
    return responses

def load_ad_reference_order():
    """Load the official AD paragraph order"""
    ref_file = Path('/home/ubuntu/canima/AD_Paragraph_Order_Reference_132.txt')
    ad_order = []
    
    with open(ref_file, 'r') as f:
        for line in f:
            match = re.search(r'\d+\.\s+AD\s+([\d.]+)', line)
            if match:
                ad_order.append(match.group(1))
    
    return ad_order

def main():
    base_path = Path('/home/ubuntu/canima')
    
    # Load AD reference order
    ad_order = load_ad_reference_order()
    ad_set = set(ad_order)
    
    # Extract existing responses
    jax_file = base_path / 'affidavits_refined' / 'Jacqueline_Answering_Affidavit_v12_FINAL.md'
    dan_file = base_path / 'affidavits_refined' / 'Daniel_Answering_Affidavit_v12_FINAL.md'
    
    jax_responses = extract_responses(jax_file, 'JR')
    dan_responses = extract_responses(dan_file, 'DR')
    
    # Create mapping
    mapping = {
        'total_ad_paragraphs': len(ad_order),
        'ad_order': ad_order,
        'jax_responses_count': len(jax_responses),
        'dan_responses_count': len(dan_responses),
        'jax_covered': list(jax_responses.keys()),
        'dan_covered': list(dan_responses.keys()),
        'jax_missing': sorted(list(ad_set - set(jax_responses.keys())), key=lambda x: [int(n) for n in x.split('.')]),
        'dan_missing': sorted(list(ad_set - set(dan_responses.keys())), key=lambda x: [int(n) for n in x.split('.')]),
        'responses': {}
    }
    
    # Map responses to AD paragraphs
    for para_num in ad_order:
        mapping['responses'][para_num] = {
            'ad_number': para_num,
            'jax_response': jax_responses.get(para_num, '[MISSING]'),
            'dan_response': dan_responses.get(para_num, '[MISSING]')
        }
    
    # Save mapping
    json_file = base_path / 'EXISTING_RESPONSES_MAPPING.json'
    with open(json_file, 'w') as f:
        json.dump(mapping, f, indent=2)
    
    # Create summary report
    report_file = base_path / 'EXISTING_RESPONSES_SUMMARY.md'
    with open(report_file, 'w') as f:
        f.write("# Existing Responses Summary\n\n")
        f.write(f"**Total AD Paragraphs:** {len(ad_order)}\n\n")
        
        f.write("## Jacqueline's Responses (JR)\n\n")
        f.write(f"- **Total responses:** {len(jax_responses)}\n")
        f.write(f"- **AD paragraphs covered:** {len(set(jax_responses.keys()) & ad_set)}\n")
        f.write(f"- **Missing paragraphs:** {len(mapping['jax_missing'])}\n\n")
        
        f.write("## Daniel's Responses (DR)\n\n")
        f.write(f"- **Total responses:** {len(dan_responses)}\n")
        f.write(f"- **AD paragraphs covered:** {len(set(dan_responses.keys()) & ad_set)}\n")
        f.write(f"- **Missing paragraphs:** {len(mapping['dan_missing'])}\n\n")
        
        f.write("## Missing from Both Affidavits\n\n")
        common_missing = sorted(list(ad_set - (set(jax_responses.keys()) | set(dan_responses.keys()))), 
                               key=lambda x: [int(n) for n in x.split('.')])
        f.write(f"**Count:** {len(common_missing)}\n\n")
        for para in common_missing:
            f.write(f"- AD {para}\n")
    
    print(f"Extraction complete:")
    print(f"  Mapping: {json_file}")
    print(f"  Summary: {report_file}")
    print(f"\nStatistics:")
    print(f"  JR responses: {len(jax_responses)} (missing {len(mapping['jax_missing'])})")
    print(f"  DR responses: {len(dan_responses)} (missing {len(mapping['dan_missing'])})")
    print(f"  Common missing: {len(common_missing)}")

if __name__ == '__main__':
    main()


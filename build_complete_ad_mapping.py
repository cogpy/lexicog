#!/usr/bin/env python3
"""
Build complete AD paragraph mapping template for affidavit refinement.
Extracts all AD paragraphs from founding affidavit and creates structured template.
"""
import re
from pathlib import Path
from collections import OrderedDict
import json

def extract_ad_paragraphs_from_founding():
    """Extract all AD paragraphs with titles and content from founding affidavit"""
    founding_file = Path('/home/ubuntu/canima/founding_affidavit/affidavit_clean.md')
    
    with open(founding_file, 'r') as f:
        content = f.read()
    
    ad_paragraphs = OrderedDict()
    
    # Pattern to match AD paragraphs like "### AD 7.1" or "## AD 1"
    # Capture paragraph number, title, and content until next AD paragraph or section
    pattern = r'###?\s+AD\s+([\d.]+)\s*\n\*([^*]+)\*\n+(.*?)(?=\n###?\s+AD\s+[\d.]+|\n##\s+[^A]|$)'
    
    matches = re.finditer(pattern, content, re.DOTALL)
    
    for match in matches:
        para_num = match.group(1)
        title = match.group(2).strip()
        body = match.group(3).strip()
        
        ad_paragraphs[para_num] = {
            'number': para_num,
            'title': title,
            'body': body[:500] + '...' if len(body) > 500 else body  # Truncate for template
        }
    
    return ad_paragraphs

def load_ad_reference_order():
    """Load the official AD paragraph order from reference file"""
    ref_file = Path('/home/ubuntu/canima/AD_Paragraph_Order_Reference_132.txt')
    ad_order = []
    
    with open(ref_file, 'r') as f:
        for line in f:
            match = re.search(r'\d+\.\s+AD\s+([\d.]+)', line)
            if match:
                ad_order.append(match.group(1))
    
    return ad_order

def create_mapping_template():
    """Create complete AD mapping template"""
    base_path = Path('/home/ubuntu/canima')
    
    # Load AD paragraphs from founding affidavit
    ad_paragraphs = extract_ad_paragraphs_from_founding()
    
    # Load official AD order
    ad_order = load_ad_reference_order()
    
    # Create JSON mapping
    mapping_data = {
        'total_ad_paragraphs': len(ad_order),
        'ad_order': ad_order,
        'ad_paragraphs': {}
    }
    
    for para_num in ad_order:
        if para_num in ad_paragraphs:
            mapping_data['ad_paragraphs'][para_num] = ad_paragraphs[para_num]
        else:
            mapping_data['ad_paragraphs'][para_num] = {
                'number': para_num,
                'title': '[NOT FOUND IN FOUNDING AFFIDAVIT]',
                'body': ''
            }
    
    # Save JSON mapping
    json_file = base_path / 'AD_COMPLETE_MAPPING_TEMPLATE.json'
    with open(json_file, 'w') as f:
        json.dump(mapping_data, f, indent=2)
    
    # Create Markdown template
    md_file = base_path / 'AD_COMPLETE_MAPPING_TEMPLATE.md'
    with open(md_file, 'w') as f:
        f.write("# Complete AD Paragraph Mapping Template\n\n")
        f.write(f"**Total AD Paragraphs:** {len(ad_order)}\n")
        f.write(f"**Extracted from Founding Affidavit:** {len(ad_paragraphs)}\n")
        f.write(f"**Missing from Founding Affidavit:** {len(ad_order) - len(ad_paragraphs)}\n\n")
        
        f.write("---\n\n")
        
        for i, para_num in enumerate(ad_order, 1):
            f.write(f"## {i}. AD {para_num}\n\n")
            
            if para_num in ad_paragraphs:
                para = ad_paragraphs[para_num]
                f.write(f"**Title:** *{para['title']}*\n\n")
                f.write(f"**Content Preview:**\n\n")
                f.write(f"> {para['body']}\n\n")
            else:
                f.write(f"**Title:** *[NOT FOUND IN FOUNDING AFFIDAVIT]*\n\n")
                f.write(f"**Content Preview:** N/A\n\n")
            
            f.write(f"**JR Response:** [TO BE ADDED]\n\n")
            f.write(f"**DR Response:** [TO BE ADDED]\n\n")
            f.write("---\n\n")
    
    print(f"Mapping template created:")
    print(f"  JSON: {json_file}")
    print(f"  Markdown: {md_file}")
    print(f"\nStatistics:")
    print(f"  Total AD paragraphs (reference): {len(ad_order)}")
    print(f"  Extracted from founding affidavit: {len(ad_paragraphs)}")
    print(f"  Missing from founding affidavit: {len(ad_order) - len(ad_paragraphs)}")
    
    return mapping_data

if __name__ == '__main__':
    mapping = create_mapping_template()


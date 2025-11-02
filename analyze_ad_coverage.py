#!/usr/bin/env python3
"""
Analyze AD paragraph coverage and sequencing in Jax and Dan's affidavits
"""
import re
from pathlib import Path
from collections import defaultdict

def extract_ad_paragraphs_from_reference(ref_file):
    """Extract all AD paragraphs from the reference file"""
    ad_list = []
    with open(ref_file, 'r') as f:
        for line in f:
            # Match lines like "  1. AD 1.1 - ..."
            match = re.search(r'\d+\.\s+AD\s+([\d.]+)', line)
            if match:
                ad_list.append(match.group(1))
    return ad_list

def extract_responses_from_affidavit(affidavit_file, prefix):
    """Extract JR/DR responses from affidavit"""
    responses = {}
    with open(affidavit_file, 'r') as f:
        content = f.read()
    
    # Match patterns like "**JR 7.13**" or "**DR 3.4.2**"
    pattern = rf'\*\*{prefix}\s+([\d.]+)\*\*'
    matches = re.finditer(pattern, content)
    
    for match in matches:
        para_num = match.group(1)
        # Get the next 500 characters to extract the title
        start = match.end()
        snippet = content[start:start+500]
        # Extract title (text between first newline and next double newline or **)
        title_match = re.search(r'\n\*([^*]+)\*', snippet)
        title = title_match.group(1).strip() if title_match else "No title"
        responses[para_num] = title
    
    return responses

def main():
    base_path = Path('/home/ubuntu/canima')
    
    # Load AD reference
    ad_ref_file = base_path / 'AD_Paragraph_Order_Reference_132.txt'
    ad_paragraphs = extract_ad_paragraphs_from_reference(ad_ref_file)
    
    print(f"Total AD paragraphs in reference: {len(ad_paragraphs)}")
    print(f"First 10: {ad_paragraphs[:10]}")
    print(f"Last 10: {ad_paragraphs[-10:]}")
    print("\n" + "="*80 + "\n")
    
    # Load Jax's responses
    jax_file = base_path / 'affidavits_refined' / 'Jacqueline_Answering_Affidavit_v12_FINAL.md'
    jax_responses = extract_responses_from_affidavit(jax_file, 'JR')
    
    print(f"Total JR responses found: {len(jax_responses)}")
    print(f"Sample JR responses:")
    for i, (para, title) in enumerate(list(jax_responses.items())[:10]):
        print(f"  JR {para}: {title[:60]}...")
    print("\n" + "="*80 + "\n")
    
    # Load Dan's responses
    dan_file = base_path / 'affidavits_refined' / 'Daniel_Answering_Affidavit_v12_FINAL.md'
    dan_responses = extract_responses_from_affidavit(dan_file, 'DR')
    
    print(f"Total DR responses found: {len(dan_responses)}")
    print(f"Sample DR responses:")
    for i, (para, title) in enumerate(list(dan_responses.items())[:10]):
        print(f"  DR {para}: {title[:60]}...")
    print("\n" + "="*80 + "\n")
    
    # Check coverage
    jax_covered = set(jax_responses.keys())
    dan_covered = set(dan_responses.keys())
    ad_set = set(ad_paragraphs)
    
    # Missing paragraphs
    jax_missing = ad_set - jax_covered
    dan_missing = ad_set - dan_covered
    
    print(f"AD paragraphs missing from Jax's affidavit: {len(jax_missing)}")
    if jax_missing:
        print(f"  Missing: {sorted(jax_missing, key=lambda x: [int(n) for n in x.split('.')])[:20]}")
    
    print(f"\nAD paragraphs missing from Dan's affidavit: {len(dan_missing)}")
    if dan_missing:
        print(f"  Missing: {sorted(dan_missing, key=lambda x: [int(n) for n in x.split('.')])[:20]}")
    
    print("\n" + "="*80 + "\n")
    
    # Check ordering
    print("Checking AD paragraph order in affidavits...")
    
    # Get ordered list of JR responses
    jax_order = list(jax_responses.keys())
    dan_order = list(dan_responses.keys())
    
    # Check if they follow AD order
    def check_order(responses_order, ad_order, name):
        """Check if responses follow AD order"""
        # Create mapping of AD para to index
        ad_index = {para: i for i, para in enumerate(ad_order)}
        
        issues = []
        for i in range(len(responses_order) - 1):
            curr = responses_order[i]
            next_para = responses_order[i + 1]
            
            if curr in ad_index and next_para in ad_index:
                if ad_index[curr] > ad_index[next_para]:
                    issues.append((i, curr, next_para))
        
        if issues:
            print(f"\n{name} ORDER ISSUES FOUND: {len(issues)}")
            for idx, curr, next_para in issues[:10]:
                print(f"  Position {idx}: {curr} comes before {next_para} (should be reversed)")
        else:
            print(f"\n{name} follows correct AD paragraph order ✓")
    
    check_order(jax_order, ad_paragraphs, "JAX")
    check_order(dan_order, ad_paragraphs, "DAN")
    
    # Save detailed report
    report_file = base_path / 'AD_COVERAGE_ANALYSIS_REPORT.md'
    with open(report_file, 'w') as f:
        f.write("# AD Paragraph Coverage Analysis Report\n\n")
        f.write(f"**Generated:** {Path(__file__).name}\n\n")
        f.write("## Summary\n\n")
        f.write(f"- Total AD paragraphs: {len(ad_paragraphs)}\n")
        f.write(f"- JR responses: {len(jax_responses)} ({len(jax_covered)/len(ad_paragraphs)*100:.1f}% coverage)\n")
        f.write(f"- DR responses: {len(dan_responses)} ({len(dan_covered)/len(ad_paragraphs)*100:.1f}% coverage)\n\n")
        
        if jax_missing:
            f.write(f"## Missing from Jax's Affidavit ({len(jax_missing)} paragraphs)\n\n")
            for para in sorted(jax_missing, key=lambda x: [int(n) for n in x.split('.')]):
                f.write(f"- AD {para}\n")
            f.write("\n")
        
        if dan_missing:
            f.write(f"## Missing from Dan's Affidavit ({len(dan_missing)} paragraphs)\n\n")
            for para in sorted(dan_missing, key=lambda x: [int(n) for n in x.split('.')]):
                f.write(f"- AD {para}\n")
            f.write("\n")
    
    print(f"\nDetailed report saved to: {report_file}")

if __name__ == '__main__':
    main()

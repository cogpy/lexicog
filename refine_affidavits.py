#!/usr/bin/env python3
"""
Refine Jax and Dan affidavits to remove hyperbole, unconfirmed claims, 
ensure factual accuracy, proper AD paragraph ordering, and complete coverage
"""
import re
from pathlib import Path
from collections import OrderedDict

def load_ad_reference():
    """Load AD paragraph reference order"""
    ad_file = Path('/home/ubuntu/canima/AD_Paragraph_Order_Reference_132.txt')
    ad_order = []
    with open(ad_file, 'r') as f:
        for line in f:
            match = re.search(r'\d+\.\s+AD\s+([\d.]+)', line)
            if match:
                ad_order.append(match.group(1))
    return ad_order

def extract_affidavit_sections(file_path, prefix):
    """Extract all response sections from affidavit"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    sections = OrderedDict()
    
    # Pattern to match response sections like **JR 7.13** or **DR 3.4.2**
    pattern = rf'\*\*{prefix}\s+([\d.]+)\*\*\s*\n\*([^*]+)\*\n(.*?)(?=\n\*\*{prefix}\s+[\d.]+\*\*|\n###|\n##|$)'
    
    matches = re.finditer(pattern, content, re.DOTALL)
    
    for match in matches:
        para_num = match.group(1)
        title = match.group(2).strip()
        body = match.group(3).strip()
        sections[para_num] = {
            'title': title,
            'body': body
        }
    
    return sections

def check_for_issues(text):
    """Check for hyperbole, speculation, and unconfirmed claims"""
    issues = []
    
    # Hyperbolic patterns
    hyperbolic_patterns = [
        (r'\b(extremely|absolutely|completely|totally|utterly|entirely)\b', 'hyperbolic_modifier'),
        (r'\b(massive|huge|enormous|catastrophic|devastating)\b', 'hyperbolic_adjective'),
        (r'\b(clearly|obviously|evidently|undoubtedly|unquestionably)\b', 'assertive_adverb'),
    ]
    
    # Speculation patterns
    speculation_patterns = [
        (r'\b(may|might|could|possibly|potentially|probably|likely)\b', 'speculation'),
        (r'\b(appears to|seems to|suggests that)\b', 'tentative_language'),
    ]
    
    # Unconfirmed claims
    unconfirmed_patterns = [
        (r'\b(I believe|I think|in my opinion)\b', 'subjective_opinion'),
        (r'\b(approximately|roughly|about|around)\s+R[\d,]+', 'approximate_amount'),
    ]
    
    for pattern, issue_type in hyperbolic_patterns + speculation_patterns + unconfirmed_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            issues.append({
                'type': issue_type,
                'text': match.group(0),
                'position': match.start()
            })
    
    return issues

def create_refinement_report():
    """Create refinement report for both affidavits"""
    base_path = Path('/home/ubuntu/canima')
    
    # Load AD reference order
    ad_order = load_ad_reference()
    ad_set = set(ad_order)
    
    # Load affidavits
    jax_file = base_path / 'affidavits_refined' / 'Jacqueline_Answering_Affidavit_v12_FINAL.md'
    dan_file = base_path / 'affidavits_refined' / 'Daniel_Answering_Affidavit_v12_FINAL.md'
    
    jax_sections = extract_affidavit_sections(jax_file, 'JR')
    dan_sections = extract_affidavit_sections(dan_file, 'DR')
    
    # Create report
    report_file = base_path / 'AFFIDAVIT_REFINEMENT_ANALYSIS.md'
    
    with open(report_file, 'w') as f:
        f.write("# Affidavit Refinement Analysis Report\n\n")
        f.write("**Case No:** 2025-137857\n")
        f.write("**Generated:** refine_affidavits.py\n\n")
        f.write("---\n\n")
        
        f.write("## 1. COVERAGE ANALYSIS\n\n")
        
        # Check coverage
        jax_covered = set(jax_sections.keys())
        dan_covered = set(dan_sections.keys())
        
        jax_missing = ad_set - jax_covered
        dan_missing = ad_set - dan_covered
        
        f.write(f"### 1.1 Jacqueline's Affidavit\n\n")
        f.write(f"- Total responses: {len(jax_sections)}\n")
        f.write(f"- AD paragraphs covered: {len(jax_covered)} / {len(ad_set)}\n")
        f.write(f"- Coverage: {len(jax_covered)/len(ad_set)*100:.1f}%\n")
        f.write(f"- Missing paragraphs: {len(jax_missing)}\n\n")
        
        if jax_missing:
            f.write("**Missing AD Paragraphs:**\n\n")
            for para in sorted(jax_missing, key=lambda x: [int(n) for n in x.split('.')]):
                f.write(f"- AD {para}\n")
            f.write("\n")
        
        f.write(f"### 1.2 Daniel's Affidavit\n\n")
        f.write(f"- Total responses: {len(dan_sections)}\n")
        f.write(f"- AD paragraphs covered: {len(dan_covered)} / {len(ad_set)}\n")
        f.write(f"- Coverage: {len(dan_covered)/len(ad_set)*100:.1f}%\n")
        f.write(f"- Missing paragraphs: {len(dan_missing)}\n\n")
        
        if dan_missing:
            f.write("**Missing AD Paragraphs:**\n\n")
            for para in sorted(dan_missing, key=lambda x: [int(n) for n in x.split('.')]):
                f.write(f"- AD {para}\n")
            f.write("\n")
        
        f.write("---\n\n")
        f.write("## 2. ORDERING ANALYSIS\n\n")
        
        # Check ordering
        def check_ordering(sections, ad_order, name):
            ad_index = {para: i for i, para in enumerate(ad_order)}
            order_issues = []
            
            section_list = list(sections.keys())
            for i in range(len(section_list) - 1):
                curr = section_list[i]
                next_para = section_list[i + 1]
                
                if curr in ad_index and next_para in ad_index:
                    if ad_index[curr] > ad_index[next_para]:
                        order_issues.append((i, curr, next_para))
            
            return order_issues
        
        jax_order_issues = check_ordering(jax_sections, ad_order, "Jacqueline")
        dan_order_issues = check_ordering(dan_sections, ad_order, "Daniel")
        
        f.write(f"### 2.1 Jacqueline's Affidavit\n\n")
        if jax_order_issues:
            f.write(f"**Ordering Issues Found:** {len(jax_order_issues)}\n\n")
            for idx, curr, next_para in jax_order_issues:
                f.write(f"- Position {idx}: JR {curr} comes before JR {next_para} (should be reversed)\n")
        else:
            f.write("✓ All responses follow correct AD paragraph order\n")
        f.write("\n")
        
        f.write(f"### 2.2 Daniel's Affidavit\n\n")
        if dan_order_issues:
            f.write(f"**Ordering Issues Found:** {len(dan_order_issues)}\n\n")
            for idx, curr, next_para in dan_order_issues:
                f.write(f"- Position {idx}: DR {curr} comes before DR {next_para} (should be reversed)\n")
        else:
            f.write("✓ All responses follow correct AD paragraph order\n")
        f.write("\n")
        
        f.write("---\n\n")
        f.write("## 3. CONTENT QUALITY ANALYSIS\n\n")
        
        # Analyze content for issues
        f.write("### 3.1 Hyperbole, Speculation, and Unconfirmed Claims\n\n")
        
        # Sample analysis on a few sections
        sample_paras = ['7.18', '8.4', '10.13', '11.8']
        
        for para in sample_paras:
            if para in jax_sections:
                issues = check_for_issues(jax_sections[para]['body'])
                if issues:
                    f.write(f"**JR {para}:** {len(issues)} potential issues\n\n")
                    for issue in issues[:5]:  # Show first 5
                        f.write(f"- {issue['type']}: '{issue['text']}'\n")
                    f.write("\n")
        
        f.write("---\n\n")
        f.write("## 4. RECOMMENDATIONS\n\n")
        
        f.write("### 4.1 Missing Paragraph Coverage\n\n")
        f.write("Both affidavits must address all 132 AD paragraphs. The following paragraphs require responses:\n\n")
        
        common_missing = jax_missing & dan_missing
        if common_missing:
            for para in sorted(common_missing, key=lambda x: [int(n) for n in x.split('.')]):
                f.write(f"- AD {para}\n")
        f.write("\n")
        
        f.write("### 4.2 Ordering Corrections\n\n")
        if jax_order_issues or dan_order_issues:
            f.write("The following sections must be reordered to follow AD paragraph sequence:\n\n")
            if jax_order_issues:
                f.write("**Jacqueline's Affidavit:**\n\n")
                for idx, curr, next_para in jax_order_issues:
                    f.write(f"- Move JR {next_para} before JR {curr}\n")
                f.write("\n")
            if dan_order_issues:
                f.write("**Daniel's Affidavit:**\n\n")
                for idx, curr, next_para in dan_order_issues:
                    f.write(f"- Move DR {next_para} before DR {curr}\n")
                f.write("\n")
        
        f.write("### 4.3 Content Refinement\n\n")
        f.write("Remove or replace the following types of language:\n\n")
        f.write("1. **Hyperbolic modifiers:** extremely, absolutely, completely, totally\n")
        f.write("2. **Assertive adverbs:** clearly, obviously, evidently, undoubtedly\n")
        f.write("3. **Speculation:** may, might, could, possibly, potentially, probably\n")
        f.write("4. **Subjective opinions:** I believe, I think, in my opinion\n")
        f.write("5. **Approximate amounts:** Replace with exact figures from evidence\n\n")
        
        f.write("### 4.4 Citation Requirements\n\n")
        f.write("Ensure all factual claims are supported by:\n\n")
        f.write("1. **Annexure references:** Cite specific annexures (e.g., 'Annexure JF1')\n")
        f.write("2. **Legal provisions:** Cite specific sections (e.g., 'Companies Act Section 162(5)(c)(ii)')\n")
        f.write("3. **Dates and amounts:** Use exact dates and amounts from evidence\n")
        f.write("4. **Timeline events:** Reference specific events from the timeline\n\n")
        
        f.write("### 4.5 Structural Improvements\n\n")
        f.write("1. **Maintain AD order:** All responses must follow the original AD paragraph sequence\n")
        f.write("2. **Complete coverage:** Address every AD paragraph, even if only to acknowledge or deny\n")
        f.write("3. **Neutral tone:** Use objective, factual language suitable for court submissions\n")
        f.write("4. **Evidence-based:** Every claim must be supported by documentary evidence\n")
        f.write("5. **Clear citations:** Reference annexures and legal provisions explicitly\n\n")
    
    print(f"Refinement analysis saved to: {report_file}")
    
    return {
        'jax_missing': jax_missing,
        'dan_missing': dan_missing,
        'jax_order_issues': jax_order_issues,
        'dan_order_issues': dan_order_issues
    }

if __name__ == '__main__':
    results = create_refinement_report()
    print("\n" + "="*80)
    print("REFINEMENT ANALYSIS COMPLETE")
    print("="*80)
    print(f"Jax missing paragraphs: {len(results['jax_missing'])}")
    print(f"Dan missing paragraphs: {len(results['dan_missing'])}")
    print(f"Jax ordering issues: {len(results['jax_order_issues'])}")
    print(f"Dan ordering issues: {len(results['dan_order_issues'])}")

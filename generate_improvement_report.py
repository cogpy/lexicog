#!/usr/bin/env python3
"""
Generate a detailed improvement report for Jax and Dan's affidavits.
"""
import re
from pathlib import Path
from collections import OrderedDict
import json

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

def extract_affidavit_responses(file_path, prefix):
    """Extract all response sections from affidavit using a more robust pattern"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    responses = OrderedDict()
    # This pattern looks for the start of a response block and captures everything until the next one or a new major section.
    pattern = rf"""(^\*\*{prefix}\s+([\d.]+)\*\*.*?)(?=\n^\*\*{prefix}\s+[\d.]+\*\*|\n^##|$)s"""
    
    matches = re.finditer(pattern, content, re.MULTILINE | re.DOTALL)
    
    for match in matches:
        para_num = match.group(2)
        full_text = match.group(1).strip()
        responses[para_num] = full_text

    return responses

def analyze_content_for_issues(text):
    """Check for hyperbole, speculation, and unconfirmed claims"""
    issues = []
    # Patterns for problematic language
    patterns = {
        'Hyperbole/Exaggeration': [r'\b(extremely|absolutely|completely|totally|utterly|entirely|massive|huge|enormous|catastrophic|devastating)\b'],
        'Assertive/Subjective Tone': [r'\b(clearly|obviously|evidently|undoubtedly|unquestionably|of course|needless to say)\b', r'\b(I believe|I think|in my opinion|it is my view)\b'],
        'Speculation': [r'\b(may|might|could|possibly|potentially|probably|likely|appears to|seems to|suggests that)\b'],
        'Vague/Imprecise Language': [r'\b(some|many|most|a few|several|various|numerous)\b', r'\b(etc\.|and so on|and the like)\b'],
        'Personal/Emotional Language': [r'\b(shock|surprise|unfortunately|sadly|happily)\b']
    }

    for issue_type, pattern_list in patterns.items():
        for pattern in pattern_list:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                # Add context to the match
                start = max(0, match.start() - 30)
                end = min(len(text), match.end() + 30)
                context = text[start:end].replace('\n', ' ')
                issues.append({
                    'type': issue_type,
                    'problematic_word': match.group(0),
                    'context': f"...{context}..."
                })
    return issues

def main():
    base_path = Path('/home/ubuntu/canima')
    report_path = base_path / 'IMPROVEMENT_RECOMMENDATIONS_V4.md'

    ad_order = load_ad_reference()
    ad_set = set(ad_order)

    jax_file = base_path / 'affidavits_refined' / 'Jacqueline_Answering_Affidavit_v12_FINAL.md'
    dan_file = base_path / 'affidavits_refined' / 'Daniel_Answering_Affidavit_v12_FINAL.md'

    jax_responses = extract_affidavit_responses(jax_file, 'JR')
    dan_responses = extract_affidavit_responses(dan_file, 'DR')

    with open(report_path, 'w') as f:
        f.write("# Affidavit Improvement Recommendations (v4)\n\n")
        f.write(f"**Generated:** {Path(__file__).name}\n")
        f.write("**Date:** 2025-11-02\n\n")
        f.write("This report provides a detailed analysis of the answering affidavits of Jacqueline Faucitt (JR) and Daniel Faucitt (DR). It identifies structural, content, and legal citation issues and offers specific recommendations for refinement to ensure the documents are robust, fact-based, and adhere to the required legal standards.\n\n")

        # --- Structural Analysis ---
        f.write("## 1. Structural Integrity Analysis\n\n")
        f.write("### 1.1. AD Paragraph Coverage\n\n")
        
        jax_covered = set(jax_responses.keys())
        dan_covered = set(dan_responses.keys())
        common_missing = sorted(list(ad_set - (jax_covered | dan_covered)), key=lambda x: [int(n) for n in x.split('.')])

        f.write("**Recommendation:** Both affidavits must address every paragraph from the Applicant's Founding Affidavit (AD). The following paragraphs are currently unaddressed and must be included.\n\n")
        if common_missing:
            f.write("| Missing AD Paragraphs |\n|:----------------------|\n")
            for para in common_missing:
                f.write(f"| AD {para}                 |\n")
        else:
            f.write("✓ All AD paragraphs appear to be covered.\n")
        f.write("\n")

        f.write("### 1.2. AD Paragraph Ordering\n\n")
        jax_order_issues = [(i, curr, jax_responses[curr][:50]) for i, curr in enumerate(jax_responses) if i > 0 and ad_order.index(curr) < ad_order.index(list(jax_responses.keys())[i-1])]
        dan_order_issues = [(i, curr, dan_responses[curr][:50]) for i, curr in enumerate(dan_responses) if i > 0 and ad_order.index(curr) < ad_order.index(list(dan_responses.keys())[i-1])]

        f.write("**Recommendation:** The responses in the affidavits must strictly follow the numerical sequence of the original AD paragraphs. The following sections are out of order and must be moved.\n\n")
        if jax_order_issues:
            f.write("**Jacqueline's Affidavit (JR):**\n")
            for i, para, text in jax_order_issues:
                f.write(f"- **JR {para}** (at position {i}) is out of sequence and should be moved to its correct position based on the AD numbering.\n")
        else:
            f.write("**Jacqueline's Affidavit (JR):** ✓ Order appears correct.\n")
        f.write("\n")
        if dan_order_issues:
            f.write("**Daniel's Affidavit (DR):**\n")
            for i, para, text in dan_order_issues:
                f.write(f"- **DR {para}** (at position {i}) is out of sequence and should be moved to its correct position based on the AD numbering.\n")
        else:
            f.write("**Daniel's Affidavit (DR):** ✓ Order appears correct.\n")
        f.write("\n")

        # --- Content Analysis ---
        f.write("## 2. Content and Tone Refinement\n\n")
        f.write("**Recommendation:** The affidavits must maintain a neutral, objective, and factual tone. All claims must be directly supported by evidence. The following examples of problematic language should be revised.\n\n")

        for name, responses in [("Jacqueline (JR)", jax_responses), ("Daniel (DR)", dan_responses)]:
            f.write(f"### 2.1. {name}\n\n")
            has_issues = False
            for para_num, text in list(responses.items())[:20]: # Sample first 20
                issues = analyze_content_for_issues(text)
                if issues:
                    has_issues = True
                    f.write(f"**Response {para_num}:**\n")
                    for issue in issues:
                        f.write(f"- **Type:** {issue['type']}\n- **Word:** `{issue['problematic_word']}`\n- **Context:** {issue['context']}\n")
                    f.write("\n")
            if not has_issues:
                f.write("✓ No significant tone issues found in the sampled sections.\n\n")

        # --- Legal & Evidentiary Analysis ---
        f.write("## 3. Legal and Evidentiary Grounding\n\n")
        f.write("**Recommendation:** Strengthen the affidavits by explicitly citing relevant annexures and legal provisions for every factual claim and legal argument.\n\n")
        f.write("### 3.1. Annexure Citation\n\n")
        f.write("For every factual claim (e.g., financial transactions, company ownership, dates), a corresponding annexure must be cited. Example:\n")
        f.write("> *On 14 and 15 February 2025, two unauthorized transfers totaling R900,000 were made from the RegimA SA FNB account (see **Annexure DR-5**, bank statements).*\n\n")

        f.write("### 3.2. Legal Citation\n\n")
        f.write("When referencing legal duties or contraventions, cite the specific section of the relevant Act. Example:\n")
        f.write("> *The Applicant's conduct constitutes a gross abuse of the position of director, in contravention of **Section 162(5)(c)(ii) of the Companies Act, 71 of 2008**.*\n\n")

        f.write("## 4. Final Checklist for Refinement\n\n")
        f.write("| Area | Action Required | Status |\n")
        f.write("|:---|:---|:---|\n")
        f.write("| **Coverage** | Address all 132 AD paragraphs. | **Action Needed** |\n")
        f.write("| **Ordering** | Re-sequence responses to match AD order. | **Action Needed** |\n")
        f.write("| **Tone** | Remove all hyperbolic, speculative, and subjective language. | **Action Needed** |\n")
        f.write("| **Evidence** | Add specific annexure citations for all factual claims. | **Action Needed** |\n")
        f.write("| **Legalities** | Add specific legal citations for all arguments. | **Action Needed** |\n")

    print(f"Improvement report generated at: {report_path}")

if __name__ == '__main__':
    main()


#!/usr/bin/env python3
"""
Reconcile the v12 affidavits with the correct 141-paragraph AD reference from the database.
Generate v13 affidavits with complete coverage of all 141 AD paragraphs.
"""
import sqlite3
from pathlib import Path

# Configuration
DB_PATH = Path("/home/ubuntu/canima/database/affidavit_data.db")
V12_JR_AFFIDAVIT = Path("/home/ubuntu/canima/affidavits_refined/Jacqueline_Answering_Affidavit_v12_FINAL.md")
V12_DR_AFFIDAVIT = Path("/home/ubuntu/canima/affidavits_refined/Daniel_Answering_Affidavit_v12_FINAL.md")
V13_JR_AFFIDAVIT = Path("/home/ubuntu/canima/affidavits_refined/Jacqueline_Answering_Affidavit_v13_FINAL.md")
V13_DR_AFFIDAVIT = Path("/home/ubuntu/canima/affidavits_refined/Daniel_Answering_Affidavit_v13_FINAL.md")

def get_all_ad_paragraphs(conn):
    """Get all 141 AD paragraphs from the database in correct order."""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT ad_number, sequence_order, section_number
        FROM ad_paragraphs_reference
        ORDER BY sequence_order
    ''')
    return cursor.fetchall()

def get_existing_responses(conn, response_type='jr'):
    """Get existing JR or DR responses from the database."""
    cursor = conn.cursor()
    table = 'jr_responses' if response_type == 'jr' else 'dr_responses'
    number_col = 'jr_number' if response_type == 'jr' else 'dr_number'
    
    cursor.execute(f'''
        SELECT {number_col}, response_text, response_type
        FROM {table}
        ORDER BY id
    ''')
    
    responses = {}
    for row in cursor.fetchall():
        number, text, resp_type = row
        if number:
            responses[number] = {'text': text, 'type': resp_type}
    
    return responses

def get_ad_content(conn, ad_number):
    """Get the content of an AD paragraph from the database."""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT content
        FROM ad_paragraphs_csv
        WHERE paragraph_number = ?
    ''', (ad_number,))
    
    result = cursor.fetchone()
    return result[0] if result else None

def generate_affidavit_v13(conn, response_type='jr'):
    """Generate a v13 affidavit with complete 141-paragraph coverage."""
    
    # Get all AD paragraphs
    all_ads = get_all_ad_paragraphs(conn)
    
    # Get existing responses
    existing_responses = get_existing_responses(conn, response_type)
    
    # Determine respondent name and prefix
    if response_type == 'jr':
        respondent_name = "Jacqueline Faucitt"
        prefix = "JR"
        title = "JACQUELINE FAUCITT'S ANSWERING AFFIDAVIT"
    else:
        respondent_name = "Daniel Faucitt"
        prefix = "DR"
        title = "DANIEL FAUCITT'S ANSWERING AFFIDAVIT"
    
    # Start building the affidavit
    affidavit = f"""# {title}

**Case No:** 2025-137857  
**Court:** High Court of South Africa, Gauteng Division, Pretoria  
**Respondent:** {respondent_name}  
**Version:** v13 FINAL (Complete 141-paragraph coverage)  
**Date:** November 2, 2025

---

## INTRODUCTION

I, the undersigned, **{respondent_name}**, do hereby make oath and state that:

1. I am an adult {'female' if response_type == 'jr' else 'male'} and the {'First' if response_type == 'jr' else 'Second'} Respondent in this matter.
2. The facts deposed to herein are within my personal knowledge and belief, save where the context indicates otherwise, and are to the best of my knowledge and belief both true and correct.
3. This affidavit is filed in response to the Applicant's Founding Affidavit and addresses each paragraph thereof in the order presented.

---

## RESPONSES TO AD PARAGRAPHS

"""
    
    # Track statistics
    covered_count = 0
    missing_count = 0
    current_section = None
    
    for ad_number, seq_order, section_number in all_ads:
        # Add section headers
        if section_number != current_section:
            current_section = section_number
            section_title = get_section_title(section_number)
            affidavit += f"\n### SECTION {section_number}: {section_title}\n\n"
        
        # Check if we have a response for this AD paragraph
        response_key = f"{ad_number}"
        
        if response_key in existing_responses:
            # Use existing response
            response_data = existing_responses[response_key]
            affidavit += f"**{prefix} {ad_number}** {response_data['text']}\n\n"
            covered_count += 1
        else:
            # Generate placeholder response
            ad_content = get_ad_content(conn, ad_number)
            if ad_content:
                affidavit += f"**{prefix} {ad_number}** [RESPONSE REQUIRED] The Applicant alleges: \"{ad_content[:200]}...\" This paragraph requires a detailed response.\n\n"
            else:
                affidavit += f"**{prefix} {ad_number}** [RESPONSE REQUIRED] This paragraph requires a detailed response.\n\n"
            missing_count += 1
    
    # Add closing
    affidavit += f"""---

## CONCLUSION

I respectfully submit that the Applicant's allegations are unfounded and that this application should be dismissed with costs.

---

**Coverage Statistics:**
- **Total AD Paragraphs:** {len(all_ads)}
- **Paragraphs Addressed:** {covered_count}
- **Paragraphs Requiring Response:** {missing_count}
- **Coverage:** {(covered_count / len(all_ads) * 100):.1f}%

---

**Signed:** {respondent_name}  
**Date:** November 2, 2025
"""
    
    return affidavit, covered_count, missing_count

def get_section_title(section_number):
    """Get the title for a section number."""
    section_titles = {
        1: "Introduction and Capacity",
        2: "Purpose of Affidavit",
        3: "Parties and Structure",
        6: "Corporate Structure",
        7: "Discovery of Financial Irregularities",
        8: "IT Expenses Analysis",
        9: "Financial Misconduct Summary",
        10: "Application to Declare Respondents Delinquent",
        11: "UK Operations",
        12: "UK Branch and Fraud Concerns",
        13: "Requirements for Interdictory Relief",
        14: "Financial Constraints and Forensic Audit",
        16: "Discovery and Urgency",
        17: "Ex Parte Basis"
    }
    return section_titles.get(section_number, f"Section {section_number}")

def main():
    print("Reconciling affidavits with database...")
    
    if not DB_PATH.exists():
        print(f"Error: Database not found at {DB_PATH}")
        return
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    
    try:
        # Generate JR affidavit v13
        print("\nGenerating Jacqueline's v13 affidavit...")
        jr_affidavit, jr_covered, jr_missing = generate_affidavit_v13(conn, 'jr')
        V13_JR_AFFIDAVIT.write_text(jr_affidavit)
        print(f"✓ Saved to {V13_JR_AFFIDAVIT}")
        print(f"  - Covered: {jr_covered}")
        print(f"  - Missing: {jr_missing}")
        print(f"  - Coverage: {(jr_covered / 141 * 100):.1f}%")
        
        # Generate DR affidavit v13
        print("\nGenerating Daniel's v13 affidavit...")
        dr_affidavit, dr_covered, dr_missing = generate_affidavit_v13(conn, 'dr')
        V13_DR_AFFIDAVIT.write_text(dr_affidavit)
        print(f"✓ Saved to {V13_DR_AFFIDAVIT}")
        print(f"  - Covered: {dr_covered}")
        print(f"  - Missing: {dr_missing}")
        print(f"  - Coverage: {(dr_covered / 141 * 100):.1f}%")
        
        print("\n✓ Reconciliation complete")
        
    finally:
        conn.close()

if __name__ == "__main__":
    main()


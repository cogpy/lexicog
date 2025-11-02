#!/usr/bin/env python3
"""
Insert Section 17 responses into the database and regenerate v14 affidavits.
"""
import sqlite3
from pathlib import Path
from datetime import datetime

# Configuration
DB_PATH = Path("/home/ubuntu/canima/database/affidavit_data.db")
V14_JR_AFFIDAVIT = Path("/home/ubuntu/canima/affidavits_refined/Jacqueline_Answering_Affidavit_v14_FINAL.md")
V14_DR_AFFIDAVIT = Path("/home/ubuntu/canima/affidavits_refined/Daniel_Answering_Affidavit_v14_FINAL.md")

# Section 17 responses
JR_RESPONSES = {
    "17.1": """I deny the Applicant's allegation and state that his purported "fear" is neither reasonable nor well-founded. It is, in fact, a self-serving and misleading justification for bringing this application on an ex parte basis, predicated on a significant material non-disclosure. The transfer of R500,000.00 was not a "defiant" act of misappropriation but a necessary and urgent operational payment made to cover immediate business expenses and creditor payments for the e-commerce operation that generates R34.9 million in annual revenue. This transfer was made necessary precisely because the Applicant, in his own "knee jerk reaction," had unilaterally and without warning cancelled 15 business credit cards on 7 June 2025, thereby crippling the companies' ability to meet their financial obligations. The Applicant materially misleads this Honourable Court by omitting the critical context: his fear of a "knee jerk reaction" is a projection of his own conduct. The Second Respondent provided the Applicant's accountant and fellow Trustee, Mr. Danie Bantjies, with comprehensive reports detailing financial misconduct on 6 June 2025. The very next day, the Applicant retaliated by cancelling the credit cards, manufacturing the very crisis he now uses to justify urgency. The Applicant's fear is therefore not based on any conduct of the Respondents, but on a situation he deliberately engineered. This is a classic application of the doctrine of *venire contra factum proprium*—the Applicant cannot be allowed to benefit from a predicament of his own making.""",
    
    "17.2": """I deny in the strongest terms that the Respondents have any intention of concealing or destroying documentation. The Applicant's alleged "reason to believe" is baseless and constitutes another material non-disclosure to this Honourable Court. The Applicant's claim is directly contradicted by the facts. On 6 June 2025, the Second Respondent, acting with full transparency, provided the Applicant's own accountant, Mr. Bantjies, with comprehensive financial reports, analyses, and supporting evidence. This act is the very antithesis of concealing or destroying documentation. The Applicant fails to disclose to this Court that the Respondents have been the party providing information, while the Applicant and his associates have been the party obfuscating it. The request for an Anton Piller-style order is not a measure to preserve evidence, but a punitive and tactical maneuver designed to harass the Respondents and seize control of the business operations under a false pretext. The Respondents have at all times acted to preserve the integrity of the companies' financial records, as it is this very evidence that exposes the misconduct which the Applicant now seeks to conceal through this urgent application.""",
    
    "17.3": """While we acknowledge the legal principle that certain applications may be brought ex parte, the Applicant's reliance on this principle is misplaced and abusive in these circumstances. An applicant approaching the court on an ex parte basis is held to the highest standard of good faith (*uberrima fides*), a duty the Applicant has manifestly failed to discharge. The Applicant has approached this Court with unclean hands, having concealed a series of material facts, any one of which should have been sufficient to persuade the Court not to grant relief without notice to the Respondents. These non-disclosures include: (a) Mr. Bantjies's Triple Conflict of Interest—The Applicant failed to disclose that his confirmatory witness, Mr. Bantjies, is not an independent accountant but is simultaneously: (i) a co-Trustee of the Faucitt Family Trust, (ii) a significant debtor to the Applicant (to the sum of R18.685 million), and (iii) the accountant for the very entities he was supposedly investigating. Furthermore, Mr. Bantjies acted as the Commissioner of Oaths for the Applicant's own affidavit, a shocking breach of legal and ethical standards. (b) The True Timeline of Events—The Applicant concealed that the alleged "discovery" of irregularities in July was false. The Second Respondent had already reported the misconduct to Mr. Bantjies on 6 June 2025, and the Applicant's subsequent card cancellations on 7 June 2025 were a direct, retaliatory response. (c) The Self-Created Urgency—The Applicant failed to disclose that the entire basis for urgency was a direct consequence of his own actions in sabotaging the companies' financial operations. The "obvious reasons" for an ex parte application do not apply when the applicant's case is built on a foundation of misrepresentation and material non-disclosure. The Applicant is not protecting the companies from the Respondents; he is protecting himself from the evidence the Respondents have compiled.""",
    
    "17.4": """I deny that the matter is urgent, and I specifically deny that there was any legitimate basis for it to be heard ex parte. The entire premise of urgency is a fabrication constructed by the Applicant to mislead this Honourable Court. The urgency was self-created. Any disruption to the business operations of the Third to Sixth Respondents was the direct and foreseeable result of the Applicant's decision to cancel the business credit cards on 7 June 2025. This act of sabotage, undertaken a single day after receiving detailed reports of financial misconduct, was the sole cause of the subsequent operational difficulties. The Applicant's true motive was not to prevent financial harm, but to launch a pre-emptive strike against the Respondents to prevent them from taking further action based on the fraud they had uncovered. This application is not a shield to protect the companies, but a sword to attack the whistleblowers. Therefore, the ex parte order was obtained through a gross abuse of the process of this Court, founded on material non-disclosures and a false narrative of urgency. We respectfully submit that the order must be set aside on this basis alone."""
}

DR_RESPONSES = {
    "17.1": """I confirm the contents of JR 17.1 and add the following facts. The Applicant's stated "fear" is disingenuous and is contradicted by the objective evidence. The R500,000.00 transfer was not a "misappropriation" but a critical operational payment required to maintain business continuity. On 7 June 2025, the Applicant cancelled 15 business credit cards (**Annexure DF4**), which were essential for paying international suppliers, software subscriptions, and hosting for the 51 e-commerce stores that generate R34.9 million in annual revenue. The transfer was a desperate measure to cover these immediate, legitimate, and verifiable business expenses. The Applicant's claim of a "knee jerk reaction" is a deliberate inversion of the truth. I personally delivered comprehensive financial reports to his accountant, Mr. Bantjies, on **6 June 2025**. The Applicant's cancellation of all credit cards occurred the very next day, on **7 June 2025**. This timeline establishes that the Applicant's action was the actual "knee jerk reaction" to the exposure of the financial misconduct detailed in my reports. The Applicant's fear is therefore not based on any rational assessment of risk, but is a self-serving narrative designed to conceal his own retaliatory conduct and to mislead this Honourable Court as to the true cause of the operational crisis.""",
    
    "17.2": """I confirm the contents of JR 17.2. The Applicant's assertion that he has "reason to believe" we would conceal or destroy documentation is a baseless and malicious falsehood. My actions prove the opposite. I am the one who compiled, preserved, and presented evidence of financial misconduct. On **6 June 2025**, I provided Mr. Bantjies with detailed reports, spreadsheets, and supporting documents. I have meticulously archived all financial data, communications, and system logs. My conduct has been one of total transparency and a commitment to preserving the evidentiary record. The request for an Anton Piller-type order is not a protective measure, but a hostile tactic. The true purpose is to seize the very evidence that I have compiled against the Applicant and his associates, and to disrupt my ability to continue managing the business and uncovering further misconduct. It is a transparent attempt to turn the tables on the whistleblower. I have a vested interest in the preservation of all documentation, as it is this documentation that will ultimately vindicate me and expose the truth. The Applicant's claim is devoid of any factual foundation and should be dismissed as the tactical maneuver that it is.""",
    
    "17.3": """I confirm the contents of JR 17.3 and wish to underscore the extent of the material non-disclosures upon which this ex parte application was founded. The Applicant failed to disclose to this Honourable Court that his key witness, Mr. Danie Bantjies, who provided a confirmatory affidavit, is hopelessly conflicted. The Applicant did not disclose that: (a) Mr. Bantjies is a co-Trustee of the Faucitt Family Trust alongside the Applicant; (b) Mr. Bantjies is a significant personal debtor to the Applicant, owing him R18.685 million as per **Annexure SF1**; (c) Mr. Bantjies was the Commissioner of Oaths for the Applicant's founding affidavit, a fundamental breach of the requirement for an independent commissioner. The Applicant presented a false timeline to the Court. He failed to disclose that he was in possession of my detailed financial reports from **6 June 2025**, and that his cancellation of the credit cards on **7 June 2025** was a direct response to those reports. He created a false impression of a recent discovery of wrongdoing in July to manufacture a sense of urgency. These are not minor omissions; they are profound misrepresentations that go to the very heart of the matter. The Applicant has fundamentally breached his duty of *uberrima fides* to this Court, and the ex parte order was granted on the basis of a deliberately incomplete and misleading set of facts.""",
    
    "17.4": """I confirm the contents of JR 17.4. The claim of urgency is a fabrication, and the evidence demonstrates that the crisis was entirely self-created by the Applicant. There was no operational urgency prior to 7 June 2025. The e-commerce businesses were functioning and profitable, generating R34.9 million in annual revenue under my management. The urgency arose as a direct and immediate consequence of the Applicant's decision to cancel 15 business credit cards on 7 June 2025. This single act crippled the companies' ability to pay for essential services, including web hosting, software subscriptions, and international suppliers. The resulting disruption was not only foreseeable but, I submit, intended. The timeline is irrefutable: I delivered reports exposing misconduct on **June 6th**. The Applicant retaliated by sabotaging the company's financial infrastructure on **June 7th**. He then approached the Court citing the very chaos he had engineered as the basis for urgent relief. This is a flagrant abuse of the court process. The matter was not urgent in the legal sense, as the Applicant had ample opportunity to address his purported concerns through ordinary legal channels. He chose not to do so, instead opting for a manufactured crisis to justify an ex parte application designed to dispossess the Respondents of control and evidence. The ex parte order, having been obtained on this false premise, must be discharged."""
}

def insert_responses(conn):
    """Insert Section 17 responses into the database."""
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Insert JR responses
    jr_count = 0
    for ad_num, response_text in JR_RESPONSES.items():
        cursor.execute('''
            INSERT OR REPLACE INTO jr_responses 
            (jr_number, response_text, created_at, updated_at, evidence_strength)
            VALUES (?, ?, ?, ?, ?)
        ''', (ad_num, response_text, timestamp, timestamp, 5))
        jr_count += 1
    
    # Insert DR responses
    dr_count = 0
    for ad_num, response_text in DR_RESPONSES.items():
        cursor.execute('''
            INSERT OR REPLACE INTO dr_responses 
            (dr_number, response_text, created_at, updated_at, evidence_strength)
            VALUES (?, ?, ?, ?, ?)
        ''', (ad_num, response_text, timestamp, timestamp, 5))
        dr_count += 1
    
    # Update reconciliation table
    for ad_num in JR_RESPONSES.keys():
        cursor.execute('''
            UPDATE ad_reconciliation
            SET has_jr_response = 1, has_dr_response = 1
            WHERE ad_number_correct = ?
        ''', (ad_num,))
    
    conn.commit()
    print(f"✓ Inserted {jr_count} JR responses")
    print(f"✓ Inserted {dr_count} DR responses")
    print(f"✓ Updated reconciliation table")

def generate_affidavit_v14(conn, response_type='jr'):
    """Generate a v14 affidavit with Section 17 responses included."""
    cursor = conn.cursor()
    
    # Get all AD paragraphs
    cursor.execute('''
        SELECT ad_number, sequence_order, section_number
        FROM ad_paragraphs_reference
        ORDER BY sequence_order
    ''')
    all_ads = cursor.fetchall()
    
    # Get existing responses
    table = 'jr_responses' if response_type == 'jr' else 'dr_responses'
    number_col = 'jr_number' if response_type == 'jr' else 'dr_number'
    
    cursor.execute(f'''
        SELECT {number_col}, response_text
        FROM {table}
        WHERE {number_col} IS NOT NULL
    ''')
    
    responses = {}
    for row in cursor.fetchall():
        number, text = row
        if number:
            responses[number] = text
    
    print(f"  Found {len(responses)} existing {response_type.upper()} responses")
    
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
**Version:** v14 FINAL (Section 17 responses added)  
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
        if ad_number in responses:
            # Use existing response
            response_text = responses[ad_number]
            affidavit += f"**{prefix} {ad_number}** {response_text}\n\n"
            covered_count += 1
        else:
            # Generate placeholder response
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
    print("Inserting Section 17 responses and generating v14 affidavits...")
    
    if not DB_PATH.exists():
        print(f"Error: Database not found at {DB_PATH}")
        return
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    
    try:
        # Insert Section 17 responses
        print("\nInserting Section 17 responses into database...")
        insert_responses(conn)
        
        # Generate JR affidavit v14
        print("\nGenerating Jacqueline's v14 affidavit...")
        jr_affidavit, jr_covered, jr_missing = generate_affidavit_v14(conn, 'jr')
        V14_JR_AFFIDAVIT.write_text(jr_affidavit)
        print(f"✓ Saved to {V14_JR_AFFIDAVIT}")
        print(f"  - Covered: {jr_covered} (+4 from v13)")
        print(f"  - Missing: {jr_missing}")
        print(f"  - Coverage: {(jr_covered / 141 * 100):.1f}%")
        
        # Generate DR affidavit v14
        print("\nGenerating Daniel's v14 affidavit...")
        dr_affidavit, dr_covered, dr_missing = generate_affidavit_v14(conn, 'dr')
        V14_DR_AFFIDAVIT.write_text(dr_affidavit)
        print(f"✓ Saved to {V14_DR_AFFIDAVIT}")
        print(f"  - Covered: {dr_covered} (+4 from v13)")
        print(f"  - Missing: {dr_missing}")
        print(f"  - Coverage: {(dr_covered / 141 * 100):.1f}%")
        
        print("\n✓ Section 17 responses successfully integrated")
        
    finally:
        conn.close()

if __name__ == "__main__":
    main()


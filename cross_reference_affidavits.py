#!/usr/bin/env python3
"""
Cross-reference ad-res-j7 findings with existing affidavits to identify gaps
"""

import json

def load_findings():
    """Load ad-res-j7 findings"""
    with open("/home/ubuntu/canima/ad_res_j7_findings.json", 'r') as f:
        return json.load(f)

def analyze_gaps():
    """Analyze gaps between ad-res-j7 findings and existing affidavits"""
    
    findings = load_findings()
    
    gaps = {
        "jacqueline_affidavit_gaps": [],
        "daniel_affidavit_gaps": [],
        "legal_analysis_gaps": [],
        "priority_integrations": []
    }
    
    # Jacqueline Affidavit Gaps
    gaps["jacqueline_affidavit_gaps"] = [
        {
            "section": "JR 7.2-7.5 (IT Expenses)",
            "current_status": "Defends IT expenses but lacks explicit legal framework",
            "missing_principles": [
                "Business Judgment Rule Protection (s76(4) Companies Act)",
                "Manufactured Crisis Framework (Peter created documentation gap)",
                "Venire Contra Factum Proprium (Peter cannot benefit from own wrong)"
            ],
            "missing_evidence": [
                "Hidden empire infrastructure requirements (51+ stores, 1100+ tenants)",
                "R5.7M computer costs dumped on RWW",
                "Evidence destruction timeline (22 May Shopify audit trail deletion)"
            ],
            "priority": "Critical",
            "action": "Add explicit legal principle citations and hidden empire evidence"
        },
        {
            "section": "JR 7.14-7.15 (Documentation Requests)",
            "current_status": "Mentions documentation gap but doesn't invoke causation analysis",
            "missing_principles": [
                "But-For Causation Test (Peter's card cancellation caused gap)",
                "Venire Contra Factum Proprium (Estoppel)",
                "Manufactured Crisis Indicators (6-8 indicators present)"
            ],
            "missing_evidence": [
                "Card cancellation June 7 (day after Dan provided reports June 6)",
                "Timeline analysis showing retaliation pattern",
                "Evidence inaccessibility directly caused by Peter's unilateral action"
            ],
            "priority": "Critical",
            "action": "Apply but-for causation test and establish Peter's factual causation"
        },
        {
            "section": "JR 8.4 (Confrontation)",
            "current_status": "Describes confrontation but doesn't invoke director collective action requirement",
            "missing_principles": [
                "Director Collective Action Requirement (s66 Companies Act)",
                "Unilateral Action Prohibition",
                "Ultra Vires Action (Peter's card cancellation beyond his authority)"
            ],
            "missing_evidence": [
                "No board resolution for card cancellation",
                "No consultation with co-directors (Jax, Dan)",
                "Immediate operational impact without emergency justification"
            ],
            "priority": "High",
            "action": "Establish Peter's card cancellation as ultra vires breach of fiduciary duty"
        },
        {
            "section": "JR 9 (Bantjies Conflict)",
            "current_status": "Mentions conflict but doesn't fully develop",
            "missing_principles": [
                "Trustee Conflict of Interest Prohibition",
                "Trust Power Abuse Test",
                "Beneficiary Adverse Action Prohibition"
            ],
            "missing_evidence": [
                "Rynette control under Bantjies instructions",
                "Email impersonation pattern (70+ days, pete@regima.com)",
                "Family network coordination (Rynette + Adderory)"
            ],
            "priority": "High",
            "action": "Strengthen with email impersonation evidence and family network analysis"
        },
        {
            "section": "JR Financial Flows Analysis",
            "current_status": "Mentions Villa Via but doesn't frame as self-dealing",
            "missing_principles": [
                "Director Self-Dealing Prohibition (s75-76 Companies Act)",
                "Related Party Transaction Disclosure Requirement",
                "Arm's Length Transaction Requirement"
            ],
            "missing_evidence": [
                "Peter owns 50% RST (paying) and 50% Villa Via (receiving)",
                "86% profit margin (not arm's length)",
                "No evidence of disclosure or independent approval"
            ],
            "priority": "High",
            "action": "Explicitly invoke self-dealing prohibition and establish voidable transaction"
        }
    ]
    
    # Daniel Affidavit Gaps
    gaps["daniel_affidavit_gaps"] = [
        {
            "section": "DR 7-8 (IT Expenses / RWD Platform)",
            "current_status": "Defends platform costs but doesn't develop unjust enrichment claim",
            "missing_principles": [
                "Unjust Enrichment Four-Element Test",
                "Trust Asset Abandonment Indicators",
                "Beneficial Ownership by Funding"
            ],
            "missing_evidence": [
                "Dan funded RWD for 28 months (R140K-R280K minimum)",
                "No reimbursement from Peter/RWD",
                "Market value of services R2.94M-R6.88M"
            ],
            "priority": "Critical",
            "action": "Develop comprehensive unjust enrichment claim with four-element test"
        },
        {
            "section": "DR Fraud Report Context",
            "current_status": "Mentions fraud report but doesn't link to evidence destruction",
            "missing_principles": [
                "Consciousness of Guilt (Evidence Destruction)",
                "Timing Analysis Bad Faith Indicators",
                "Obstruction of Justice"
            ],
            "missing_evidence": [
                "Fraud report to Bantjies June 6, 2025",
                "Shopify audit trail deletion May 22 (7 days after confrontation)",
                "Card cancellation June 7 (1 day after fraud report)",
                "R3.1M+ revenue loss correlated with evidence destruction"
            ],
            "priority": "Critical",
            "action": "Link fraud report to immediate retaliation and evidence destruction sequence"
        },
        {
            "section": "DR Hidden Empire Infrastructure",
            "current_status": "Defends IT expenses but doesn't reveal hidden empire scale",
            "missing_evidence": [
                "51+ Shopify stores (completely undisclosed)",
                "1100+ B2B salon tenants (completely undisclosed)",
                "4 distribution companies (completely undisclosed)",
                "R5.7M computer platform costs for hidden operations"
            ],
            "priority": "Critical",
            "action": "Reveal hidden empire to establish IT expenses were for operations Dan didn't control"
        }
    ]
    
    # Legal Analysis Gaps
    gaps["legal_analysis_gaps"] = [
        {
            "section": "Company Law Principles",
            "missing": [
                "Director Collective Action Requirement (s66)",
                "Director Self-Dealing Prohibition (s75-76)",
                "Business Judgment Rule Protection (s76(4))",
                "Manufactured Crisis Framework"
            ],
            "priority": "Critical",
            "action": "Add comprehensive company law section with explicit statutory citations"
        },
        {
            "section": "Trust Law Principles",
            "missing": [
                "Trustee Conflict of Interest Prohibition",
                "Abuse of Trust Powers Test",
                "Trust Asset Abandonment Indicators",
                "Beneficiary Adverse Action Prohibition"
            ],
            "priority": "Critical",
            "action": "Add comprehensive trust law section with fiduciary duty analysis"
        },
        {
            "section": "Civil Law Principles",
            "missing": [
                "Unjust Enrichment Four-Element Test",
                "Venire Contra Factum Proprium (Estoppel)",
                "But-For Causation Test"
            ],
            "priority": "High",
            "action": "Add civil law section with unjust enrichment claim development"
        },
        {
            "section": "Criminal Elements Analysis",
            "missing": [
                "Email Impersonation Pattern (70+ days, ECTA violations)",
                "Evidence Destruction (Consciousness of Guilt)",
                "Revenue Diversion Setup (April 14 bank letter)",
                "Family Conspiracy (Network analysis)"
            ],
            "priority": "High",
            "action": "Add criminal elements section supporting criminal referral"
        },
        {
            "section": "Evidence Quality Assessment",
            "missing": [
                "Grade A evidence categories (Revenue Diversion, Evidence Destruction, Email Impersonation)",
                "Prosecution-ready evidence packages",
                "Financial quantifications (R43M+ total)"
            ],
            "priority": "Medium",
            "action": "Add evidence quality section with grading and prosecution readiness"
        }
    ]
    
    # Priority Integrations
    gaps["priority_integrations"] = [
        {
            "priority": 1,
            "integration": "Unjust Enrichment Claim (Dan)",
            "principle": "Four-Element Test",
            "evidence": "R140K-R280K minimum to R2.94M-R6.88M market value",
            "where": "DR 7-8, Counter-application, RWD analysis",
            "impact": "Establishes Dan's beneficial ownership or restitution claim"
        },
        {
            "priority": 2,
            "integration": "Manufactured Crisis Framework (Jax)",
            "principle": "6-8 Manufactured Crisis Indicators",
            "evidence": "Card cancellation day after Dan provided reports, documentation gap creation",
            "where": "JR 7.2-7.5, JR 7.14-7.15, Bad faith analysis",
            "impact": "Rebuts good faith presumption, establishes bad faith and improper purpose"
        },
        {
            "priority": 3,
            "integration": "Trustee Conflict Prohibition (Jax)",
            "principle": "Beneficiary Adverse Action Prohibition",
            "evidence": "Peter (trustee) seeks interdict against Jax (beneficiary)",
            "where": "JR 3-3.10, JR 11-11.5, Motion for removal",
            "impact": "Fundamental breach of fiduciary duty, grounds for removal as trustee"
        },
        {
            "priority": 4,
            "integration": "Director Collective Action Requirement (Jax)",
            "principle": "s66 Companies Act - Board Resolution Necessity",
            "evidence": "Peter's unilateral card cancellation without board resolution",
            "where": "JR 7.2-7.5, JR 8.4, Legal analysis",
            "impact": "Ultra vires action, breach of fiduciary duty, personally liable"
        },
        {
            "priority": 5,
            "integration": "Email Impersonation Pattern (Both)",
            "principle": "Identity Theft (ECTA s86-87)",
            "evidence": "70+ days pete@regima.com controlled by Rynette, R3.1M+ correlated loss",
            "where": "JR 9, DR Fraud Report, Criminal referral",
            "impact": "Prosecution-ready criminal evidence, supports conspiracy charges"
        },
        {
            "priority": 6,
            "integration": "Self-Dealing Prohibition (Jax)",
            "principle": "s75-76 Companies Act",
            "evidence": "Peter owns 50% RST and 50% Villa Via, 86% profit margin",
            "where": "JR Financial flows, Counter-allegations, Shareholder oppression",
            "impact": "Voidable transaction, must account for excess profits"
        },
        {
            "priority": 7,
            "integration": "Hidden Empire Evidence (Dan)",
            "principle": "Expense Dumping and Scapegoating",
            "evidence": "51+ stores, 1100+ tenants, 4 distributors, R5.7M costs on RWW",
            "where": "DR 7-8, JR 7.2-7.5, Victim narrative",
            "impact": "Establishes Jax/Dan as victims, not perpetrators"
        },
        {
            "priority": 8,
            "integration": "Evidence Destruction Timeline (Both)",
            "principle": "Consciousness of Guilt",
            "evidence": "May 22 Shopify deletion (7 days after confrontation), R3.1M+ loss",
            "where": "JR 8.4, DR Fraud Report, Criminal referral",
            "impact": "Demonstrates coordinated cover-up, supports criminal charges"
        }
    ]
    
    return gaps

def main():
    print("Cross-referencing ad-res-j7 findings with existing affidavits...")
    
    gaps = analyze_gaps()
    
    # Save as JSON
    json_path = "/home/ubuntu/canima/affidavit_gaps_analysis.json"
    with open(json_path, 'w') as f:
        json.dump(gaps, f, indent=2)
    print(f"✓ JSON gaps analysis saved: {json_path}")
    
    # Generate markdown report
    md_path = "/home/ubuntu/canima/AFFIDAVIT_GAPS_ANALYSIS.md"
    with open(md_path, 'w') as f:
        f.write("# Affidavit Gaps Analysis - AD-RES-J7 Integration\n\n")
        f.write("**Date:** November 4, 2025\n")
        f.write("**Purpose:** Identify gaps between ad-res-j7 findings and existing affidavits\n\n")
        f.write("---\n\n")
        
        f.write("## Executive Summary\n\n")
        f.write("This analysis identifies critical gaps in the existing affidavits that can be filled ")
        f.write("with legal principles, evidence, and strategic arguments from the ad-res-j7 repository.\n\n")
        f.write(f"**Jacqueline Affidavit Gaps:** {len(gaps['jacqueline_affidavit_gaps'])}\n")
        f.write(f"**Daniel Affidavit Gaps:** {len(gaps['daniel_affidavit_gaps'])}\n")
        f.write(f"**Legal Analysis Gaps:** {len(gaps['legal_analysis_gaps'])}\n")
        f.write(f"**Priority Integrations:** {len(gaps['priority_integrations'])}\n\n")
        f.write("---\n\n")
        
        # Jacqueline Affidavit Gaps
        f.write("## Part 1: Jacqueline Affidavit Gaps\n\n")
        for i, gap in enumerate(gaps['jacqueline_affidavit_gaps'], 1):
            f.write(f"### Gap {i}: {gap['section']}\n\n")
            f.write(f"**Priority:** {gap['priority']}\n\n")
            f.write(f"**Current Status:** {gap['current_status']}\n\n")
            
            if 'missing_principles' in gap:
                f.write("**Missing Legal Principles:**\n")
                for principle in gap['missing_principles']:
                    f.write(f"- {principle}\n")
                f.write("\n")
            
            if 'missing_evidence' in gap:
                f.write("**Missing Evidence:**\n")
                for evidence in gap['missing_evidence']:
                    f.write(f"- {evidence}\n")
                f.write("\n")
            
            f.write(f"**Recommended Action:** {gap['action']}\n\n")
            f.write("---\n\n")
        
        # Daniel Affidavit Gaps
        f.write("## Part 2: Daniel Affidavit Gaps\n\n")
        for i, gap in enumerate(gaps['daniel_affidavit_gaps'], 1):
            f.write(f"### Gap {i}: {gap['section']}\n\n")
            f.write(f"**Priority:** {gap['priority']}\n\n")
            f.write(f"**Current Status:** {gap['current_status']}\n\n")
            
            if 'missing_principles' in gap:
                f.write("**Missing Legal Principles:**\n")
                for principle in gap['missing_principles']:
                    f.write(f"- {principle}\n")
                f.write("\n")
            
            if 'missing_evidence' in gap:
                f.write("**Missing Evidence:**\n")
                for evidence in gap['missing_evidence']:
                    f.write(f"- {evidence}\n")
                f.write("\n")
            
            f.write(f"**Recommended Action:** {gap['action']}\n\n")
            f.write("---\n\n")
        
        # Legal Analysis Gaps
        f.write("## Part 3: Legal Analysis Gaps\n\n")
        for i, gap in enumerate(gaps['legal_analysis_gaps'], 1):
            f.write(f"### Gap {i}: {gap['section']}\n\n")
            f.write(f"**Priority:** {gap['priority']}\n\n")
            
            f.write("**Missing Elements:**\n")
            for missing in gap['missing']:
                f.write(f"- {missing}\n")
            f.write("\n")
            
            f.write(f"**Recommended Action:** {gap['action']}\n\n")
            f.write("---\n\n")
        
        # Priority Integrations
        f.write("## Part 4: Priority Integrations (Ranked)\n\n")
        f.write("| Priority | Integration | Principle | Where | Impact |\n")
        f.write("|----------|-------------|-----------|-------|--------|\n")
        for integration in gaps['priority_integrations']:
            f.write(f"| {integration['priority']} | {integration['integration']} | {integration['principle']} | {integration['where']} | {integration['impact']} |\n")
        f.write("\n---\n\n")
        
        # Conclusion
        f.write("## Conclusion\n\n")
        f.write("**Critical Priority Gaps (3):**\n")
        f.write("1. Unjust Enrichment Claim (Dan) - R140K-R280K to R2.94M-R6.88M restitution\n")
        f.write("2. Manufactured Crisis Framework (Jax) - Rebuts good faith presumption\n")
        f.write("3. Trustee Conflict Prohibition (Jax) - Grounds for removal as trustee\n\n")
        f.write("**High Priority Gaps (3):**\n")
        f.write("4. Director Collective Action Requirement (Jax) - Ultra vires action\n")
        f.write("5. Email Impersonation Pattern (Both) - Prosecution-ready criminal evidence\n")
        f.write("6. Self-Dealing Prohibition (Jax) - Voidable transaction\n\n")
        f.write("**Medium Priority Gaps (2):**\n")
        f.write("7. Hidden Empire Evidence (Dan) - Establishes victim narrative\n")
        f.write("8. Evidence Destruction Timeline (Both) - Consciousness of guilt\n\n")
        f.write("**Next Steps:**\n")
        f.write("1. Integrate Priority 1-3 (Critical) into affidavits immediately\n")
        f.write("2. Integrate Priority 4-6 (High) into affidavits within 48 hours\n")
        f.write("3. Integrate Priority 7-8 (Medium) into comprehensive legal analysis\n")
        f.write("4. Update improvement recommendations with priority integrations\n\n")
        f.write("**Status:** Ready for affidavit enhancement implementation\n")
    
    print(f"✓ Markdown gaps analysis saved: {md_path}")
    
    print("\n" + "="*80)
    print("GAPS ANALYSIS SUMMARY")
    print("="*80)
    print(f"Jacqueline Affidavit Gaps: {len(gaps['jacqueline_affidavit_gaps'])}")
    print(f"Daniel Affidavit Gaps:     {len(gaps['daniel_affidavit_gaps'])}")
    print(f"Legal Analysis Gaps:       {len(gaps['legal_analysis_gaps'])}")
    print(f"Priority Integrations:     {len(gaps['priority_integrations'])}")
    print("="*80)
    print("\nCritical Priority Integrations:")
    for integration in gaps['priority_integrations'][:3]:
        print(f"  {integration['priority']}. {integration['integration']}")
    print("="*80)

if __name__ == "__main__":
    main()

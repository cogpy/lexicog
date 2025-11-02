#!/usr/bin/env python3
"""
Extract entities, relations, events, and timelines from legal documents
"""
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import json

def extract_entities():
    """Extract key entities from the case"""
    entities = {
        "persons": {
            "Peter Andrew Faucitt": {
                "id": "520430 5708 18 5",
                "role": "Applicant, Director, Trustee",
                "companies": ["RegimA SA", "RegimA Worldwide", "Villa Via", "Strategic Logistics"]
            },
            "Jacqueline Faucitt": {
                "id": "570607 0898 18 1",
                "role": "First Respondent, Director, Trustee, CEO RegimA Skin Treatments",
                "companies": ["RegimA SA", "RegimA Worldwide"]
            },
            "Daniel James Faucitt": {
                "id": "820715 5300 18 2",
                "role": "Second Respondent, Director, CIO, Beneficiary",
                "companies": ["RegimA SA", "RegimA Worldwide", "RegimA Zone Ltd (UK)"]
            },
            "Danie Jacobus Bantjies": {
                "role": "Accountant, Third Trustee (undisclosed), Debtor (R18.685M), Commissioner of Oaths",
                "company": "Bantjes and Company",
                "conflict": "Trustee + Debtor + Accountant + Company Controller"
            },
            "Rynette Farrar": {
                "role": "Financial Controller, Sage System Operator",
                "control": "All bank accounts, Sage accounting using pete@regima.com",
                "family": "Sister: Linda (bookkeeper), Son: owns Adderory (Pty) Ltd"
            },
            "Kayla Pretorius": {
                "role": "Dan's partner, Co-builder of Shopify operations",
                "status": "Murdered 13 July 2023",
                "estate": "Rezonance, owed R1,035,000 by RegimA Skin Treatments"
            }
        },
        "companies": {
            "RegimA Skin Treatments CC": {
                "reg": "1992/005371/23",
                "type": "Close Corporation",
                "debt": "R1,035,000 to Rezonance (Kayla's estate) since Feb 2023",
                "supplier": "Adderory (Pty) Ltd (Rynette's son's company)"
            },
            "RegimA Worldwide Distribution (Pty) Ltd": {
                "reg": "2011/005722/07",
                "type": "Private Company",
                "owner": "Faucitt Family Trust (IT 3651/2013)",
                "directors": "Jax, Dan (co-directors)",
                "sabotage": "Revenue diversion started 14 Apr 2025 (ABSA bank letter)"
            },
            "Villa Via Arcadia No 2 CC": {
                "reg": "1996/004451/23",
                "type": "Close Corporation",
                "owner": "Faucitt Family Trust",
                "fraud": "86% profit margin on rent - excessive profit extraction",
                "exposed": "6 June 2025 by Dan to Bantjies"
            },
            "Strategic Logistics CC": {
                "reg": "2008/136496/23",
                "type": "Close Corporation",
                "fraud": "R5.4M stock adjustment (46% of R11.3M annual sales)",
                "stock_type": "Matches Adderory inventory supplied to RegimA Skin Treatments"
            },
            "RegimA Zone Ltd": {
                "reg": "UK 10697009",
                "type": "UK Company",
                "owner": "Dan (independent of RegimA UK Ltd)",
                "operations": "Owns and funds 51+ Shopify platforms",
                "revenue": "R34.9M annually (RegimA SA: R8.5M, RegimA Zone: R26.4M)"
            },
            "Adderory (Pty) Ltd": {
                "owner": "Rynette's son",
                "actions": [
                    "Supplies stock to RegimA Skin Treatments",
                    "Registered regimaskin.co.za on 29 May 2025",
                    "Diverted customers from Dan's platforms"
                ]
            },
            "Faucitt Family Trust": {
                "reg": "IT 3651/2013",
                "trustees": ["Peter (Founder)", "Jax", "Danie Bantjies (undisclosed)"],
                "beneficiaries": ["Jax", "Dan"],
                "owns": ["RegimA Worldwide", "Villa Via"],
                "debt_owed_by_trustee": "Bantjies owes R18.685M (payout: May 2026, 2027, 2029)"
            }
        },
        "banks": {
            "FirstRand Bank (FNB)": {
                "unauthorized_transfers": "R900,000 (14-15 Feb 2025)",
                "account_depletion": "R997,597.94 to R5,284.08 in one month",
                "active_trade": "169 customer deposits totaling R566,598.57"
            },
            "ABSA Bank": {
                "accounts": "8 accounts possibly opened by Rynette using Dan's info",
                "revenue_diversion": "Started 14 Apr 2025 for RegimA Worldwide"
            }
        }
    }
    return entities

def extract_timeline():
    """Extract critical timeline events"""
    timeline = [
        {"date": "2023-02-01", "event": "RegimA Skin Treatments debt to Rezonance begins", "amount": "R1,035,000", "parties": ["RegimA Skin Treatments", "Rezonance"]},
        {"date": "2023-07-13", "event": "Kayla Pretorius murdered", "parties": ["Kayla Pretorius"]},
        {"date": "2025-02-14", "event": "Unauthorized transfer from RegimA SA FNB account", "amount": "R450,000", "parties": ["FNB", "Dan"]},
        {"date": "2025-02-15", "event": "Second unauthorized transfer from RegimA SA FNB account", "amount": "R450,000", "parties": ["FNB", "Dan"]},
        {"date": "2025-03-01", "event": "Revenue diversion for RegimA SA begins", "parties": ["RegimA SA", "Rynette"]},
        {"date": "2025-03-30", "event": "Rynette and Peter dump 2 years unallocated expenses into RWD, demand Dan sign off in 12 hours", "parties": ["Rynette", "Peter", "Dan", "RWD"]},
        {"date": "2025-04-14", "event": "ABSA bank letter - Revenue diversion for RegimA Worldwide begins", "parties": ["ABSA", "RegimA Worldwide", "Rynette"]},
        {"date": "2025-05-15", "event": "Jax confronts Rynette about R1,035,000 debt - 'profiting from proceeds of murder'", "parties": ["Jax", "Rynette", "RegimA Skin Treatments", "Rezonance"]},
        {"date": "2025-05-22", "event": "Shopify data expunged (100% audit data loss)", "impact": "7 days after Jax's confrontation", "parties": ["Dan", "Shopify"]},
        {"date": "2025-05-29", "event": "Domain regimaskin.co.za registered by Adderory", "impact": "14 days after Jax's confrontation", "parties": ["Adderory", "Rynette"]},
        {"date": "2025-06-06", "event": "Dan provides comprehensive reports to Bantjies, exposes Villa Via fraud", "parties": ["Dan", "Bantjies", "Villa Via"]},
        {"date": "2025-06-07", "event": "Peter cancels 15 UK business cards without notice", "impact": "1 day after Dan's cooperation", "parties": ["Peter", "Dan"]},
        {"date": "2025-06-10", "event": "Bantjies dismisses Dan's audit request - 'going on holiday'", "parties": ["Bantjies", "Dan"]},
        {"date": "2025-06-20", "event": "Gee instructed to send 'don't use regima.zone only use regimaskin.co.za' email", "parties": ["Gee", "Rynette", "Adderory"]},
        {"date": "2025-07-08", "event": "Warehouse sabotage - R34.9M operations destroyed", "parties": ["Dan", "RegimA Zone"]},
        {"date": "2025-07-16", "event": "Jax transfers R500,000 to Dan as 'birthday gift' without Peter's authorization", "parties": ["Jax", "Dan", "Peter"]},
        {"date": "2025-08-19", "event": "Ex parte order granted", "parties": ["Peter", "Court"]},
        {"date": "2025-09-11", "event": "R1.73M transferred from accounts", "impact": "6 months after sabotage began, Dan still managing to pay creditors", "parties": ["Dan", "Creditors"]}
    ]
    return timeline

def extract_legal_aspects():
    """Extract relevant legal aspects and citations"""
    legal_aspects = {
        "Companies Act 71 of 2008": {
            "Section 162(2)": "Locus standi for directors/shareholders",
            "Section 162(5)(c)(ii)": "Grossly abused position of director/member",
            "Section 162(5)(c)(iii)": "Intentionally or by gross negligence inflicted harm",
            "Section 162(5)(c)(iv)": "Gross negligence, wilful misconduct, breach of trust",
            "Section 162(a)(iii)": "Oppressive or unfairly prejudicial conduct",
            "Section 42(2)(a)(ii)": "Director shall not exceed powers",
            "Section 77(3)(b)": "Acquiescence in conduct"
        },
        "Trust Property Control Act": {
            "Section 9(1)": "Trustees must act with care, diligence, and skill in interests of beneficiaries"
        },
        "Legal Principles": {
            "venire contra factum proprium": "Acting contrary to one's own previous conduct (Peter created problem he complains about)",
            "anton piller order": "Ex parte application to prevent destruction of evidence",
            "conflict of interest": "Bantjies: Trustee + Debtor + Accountant + Company Controller"
        }
    }
    return legal_aspects

def extract_financial_evidence():
    """Extract key financial evidence"""
    financial = {
        "IT Expenses (Peter's claims)": {
            "2024_tax_year": "R6,738,007.47",
            "2025_tax_year": "R2,116,159.47",
            "context_omitted": "Supported 51+ Shopify stores generating R34.9M annually",
            "percentage_of_revenue_2024": "19.3%",
            "percentage_of_revenue_2025": "6.1%"
        },
        "Revenue Performance": {
            "RegimA_SA": "25 stores, R8.5M turnover",
            "RegimA_Zone": "26 stores, R26.4M turnover",
            "Total": "51+ stores, R34.9M annually"
        },
        "Fraudulent Transactions": {
            "Unauthorized_FNB_transfers": "R900,000 (14-15 Feb 2025)",
            "Birthday_gift": "R500,000 (16 July 2025, unauthorized)",
            "Stock_adjustment_SLG": "R5.4M (46% of R11.3M sales)",
            "Villa_Via_fraud": "86% profit margin on rent",
            "RegimA_debt_to_Kayla_estate": "R1,035,000 (since Feb 2023)"
        },
        "Bantjies Debt": {
            "amount": "R18,685,000",
            "payout_schedule": "May 2026, 2027, 2029",
            "conflict": "Debtor to trust while serving as trustee and accountant"
        }
    }
    return financial

def main():
    base_path = Path('/home/ubuntu/canima')
    
    # Extract all data
    entities = extract_entities()
    timeline = extract_timeline()
    legal_aspects = extract_legal_aspects()
    financial = extract_financial_evidence()
    
    # Create comprehensive report
    report = {
        "entities": entities,
        "timeline": timeline,
        "legal_aspects": legal_aspects,
        "financial_evidence": financial
    }
    
    # Save as JSON
    json_file = base_path / 'LEGAL_ENTITIES_RELATIONS_TIMELINE.json'
    with open(json_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    # Create markdown report
    md_file = base_path / 'LEGAL_ENTITIES_RELATIONS_TIMELINE.md'
    with open(md_file, 'w') as f:
        f.write("# Legal Entities, Relations, Events & Timeline Analysis\n\n")
        f.write("**Case No:** 2025-137857\n")
        f.write("**Court:** High Court of South Africa, Gauteng Division, Pretoria\n\n")
        f.write("---\n\n")
        
        # Entities section
        f.write("## 1. ENTITIES\n\n")
        
        f.write("### 1.1 Natural Persons\n\n")
        for name, details in entities["persons"].items():
            f.write(f"**{name}**\n\n")
            for key, value in details.items():
                if isinstance(value, list):
                    f.write(f"- {key}: {', '.join(value)}\n")
                else:
                    f.write(f"- {key}: {value}\n")
            f.write("\n")
        
        f.write("### 1.2 Corporate Entities\n\n")
        for name, details in entities["companies"].items():
            f.write(f"**{name}**\n\n")
            for key, value in details.items():
                if isinstance(value, list):
                    for item in value:
                        f.write(f"- {item}\n")
                else:
                    f.write(f"- {key}: {value}\n")
            f.write("\n")
        
        f.write("### 1.3 Financial Institutions\n\n")
        for name, details in entities["banks"].items():
            f.write(f"**{name}**\n\n")
            for key, value in details.items():
                f.write(f"- {key}: {value}\n")
            f.write("\n")
        
        # Timeline section
        f.write("## 2. CRITICAL TIMELINE\n\n")
        f.write("| Date | Event | Parties | Amount/Impact |\n")
        f.write("|:-----|:------|:--------|:--------------|\n")
        for event in timeline:
            date = event.get("date", "")
            evt = event.get("event", "")
            parties = ", ".join(event.get("parties", []))
            amount = event.get("amount", event.get("impact", ""))
            f.write(f"| {date} | {evt} | {parties} | {amount} |\n")
        
        f.write("\n")
        
        # Legal aspects section
        f.write("## 3. LEGAL ASPECTS\n\n")
        for statute, sections in legal_aspects.items():
            f.write(f"### 3.1 {statute}\n\n")
            for section, description in sections.items():
                f.write(f"**{section}:** {description}\n\n")
        
        # Financial evidence section
        f.write("## 4. FINANCIAL EVIDENCE\n\n")
        for category, details in financial.items():
            f.write(f"### 4.1 {category.replace('_', ' ')}\n\n")
            if isinstance(details, dict):
                for key, value in details.items():
                    f.write(f"- **{key.replace('_', ' ')}:** {value}\n")
            f.write("\n")
        
        # Relations section
        f.write("## 5. KEY RELATIONSHIPS & CONFLICTS\n\n")
        f.write("### 5.1 Bantjies Conflict of Interest\n\n")
        f.write("Danie Jacobus Bantjies occupies four conflicting roles:\n\n")
        f.write("1. **Trustee** of Faucitt Family Trust (undisclosed to beneficiaries)\n")
        f.write("2. **Debtor** owing R18.685M to the trust\n")
        f.write("3. **Accountant** for all companies (Bantjes and Company)\n")
        f.write("4. **Company Controller** giving instructions to Rynette for multi-million rand transactions\n\n")
        f.write("**Legal Issue:** This creates an impermissible conflict under Trust Property Control Act Section 9(1) and Companies Act fiduciary duties.\n\n")
        
        f.write("### 5.2 Rynette Control Structure\n\n")
        f.write("Rynette Farrar controls:\n\n")
        f.write("- All bank accounts (Peter had no access)\n")
        f.write("- Sage accounting system using Peter's email (pete@regima.com)\n")
        f.write("- Claims to act under Bantjies's instructions, not Peter's\n\n")
        f.write("**Family Connection:** Sister Linda employed as bookkeeper, yet 2 years expenses unallocated until 30 March 2025\n\n")
        f.write("**Son's Company:** Adderory (Pty) Ltd supplies stock to RegimA Skin Treatments and registered competing domain regimaskin.co.za\n\n")
        
        f.write("### 5.3 Revenue Diversion Pattern\n\n")
        f.write("Systematic sabotage timeline:\n\n")
        f.write("1. **15 May 2025:** Jax confronts Rynette about R1.035M debt\n")
        f.write("2. **22 May 2025:** Shopify data expunged (7 days later)\n")
        f.write("3. **29 May 2025:** Competing domain registered (14 days later)\n")
        f.write("4. **6 June 2025:** Dan exposes Villa Via fraud to Bantjies\n")
        f.write("5. **7 June 2025:** Peter cancels cards (1 day later)\n")
        f.write("6. **20 June 2025:** Customer diversion email sent\n")
        f.write("7. **8 July 2025:** Warehouse sabotage\n\n")
        
        f.write("**Pattern:** Each sabotage action follows either Jax's debt inquiry or Dan's fraud exposure.\n\n")
        
        f.write("### 5.4 Venire Contra Factum Proprium\n\n")
        f.write("Peter's actions demonstrate acting contrary to his own previous conduct:\n\n")
        f.write("- Cancelled cards on 7 June 2025 (one day after Dan's cooperation)\n")
        f.write("- Card cancellation rendered documentation inaccessible (card-based authentication)\n")
        f.write("- Then complained about missing documentation\n")
        f.write("- Created the problem he now complains about in the interdict application\n\n")
    
    print(f"Legal entities, relations, and timeline analysis saved to:")
    print(f"  - JSON: {json_file}")
    print(f"  - Markdown: {md_file}")
    
    # Print summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Persons identified: {len(entities['persons'])}")
    print(f"Companies identified: {len(entities['companies'])}")
    print(f"Timeline events: {len(timeline)}")
    print(f"Legal statutes/principles: {sum(len(v) for v in legal_aspects.values())}")
    print(f"Financial categories: {len(financial)}")

if __name__ == '__main__':
    main()

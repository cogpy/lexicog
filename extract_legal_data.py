#!/usr/bin/env python3
"""
Extract entities, relations, events, and timelines from legal documents
"""
import json
import re
from datetime import datetime
from pathlib import Path

# Define entities structure
entities = {
    "persons": {
        "Peter Andrew Faucitt": {
            "id_number": "520430 5708 18 5",
            "roles": ["Applicant", "Trustee of Faucitt Family Trust", "Creditor to Bantjies"],
            "address": "20 River Road, Morning Hill, Bedfordview"
        },
        "Jacqueline Faucitt": {
            "id_number": "570607 0898 18 1",
            "roles": ["First Respondent", "Co-trustee of Faucitt Family Trust", "Co-director RegimA SA", "Beneficiary"],
            "address": "20 River Road, Morning Hill, Bedfordview"
        },
        "Daniel James Faucitt": {
            "id_number": "900815 5300 08 9",
            "roles": ["Second Respondent", "Co-director RegimA SA", "Co-director RegimA Worldwide", "Beneficiary", "Built 51+ Shopify stores"],
            "business_built": "R34.9M e-commerce operation"
        },
        "Danie Jacobus Bantjies": {
            "roles": ["Accountant", "Third Trustee (concealed)", "Debtor to Peter (R18.685M)", "Company Controller", "Commissioner of Oaths"],
            "company": "Bantjes and Company CA(SA)",
            "debt": "R18.685M (May 2026, 2027, 2029 payout schedule)",
            "conflict": "Trustee + Debtor + Accountant + Company Controller"
        },
        "Rynette Farrar": {
            "roles": ["Administrator", "Controller of email accounts", "Controller of Sage system", "Controller of bank accounts"],
            "control": ["All bank accounts", "Sage system using pete@regima.com", "Email accounts"],
            "sister": "Linda (bookkeeper)",
            "son_company": "Adderory (Pty) Ltd"
        },
        "Kayla Pretorius": {
            "roles": ["Co-builder of e-commerce operations", "Deceased"],
            "death_date": "13 July 2023",
            "estate_company": "Rezonance (Pty) Ltd",
            "estate_debt_owed": "R1,035,000 by RegimA Skin Treatments since Feb 2023"
        }
    },
    "companies": {
        "RegimA Skin Treatments CC": {
            "registration": "B1992/005371/23",
            "debt": "R1,035,000 to Rezonance (Kayla's estate) since Feb 2023",
            "stock_supplier": "Adderory (Pty) Ltd (Rynette's son's company)"
        },
        "RegimA SA (Pty) Ltd": {
            "registration": "2017/087935/07",
            "directors": ["Jacqueline Faucitt", "Daniel Faucitt"],
            "shopify_stores": 25,
            "turnover": "R8.5M",
            "unauthorized_transfers": "R900,000 (14-15 Feb 2025)",
            "revenue_diversion_start": "1 Mar 2025"
        },
        "RegimA Worldwide Distribution (Pty) Ltd": {
            "registration": "2011/005722/07",
            "owner": "Faucitt Family Trust",
            "directors": ["Jacqueline Faucitt", "Daniel Faucitt"],
            "revenue_diversion_start": "14 Apr 2025 (ABSA bank letter)"
        },
        "RegimA Zone Ltd": {
            "registration": "UK company 10697009",
            "owner": "Daniel Faucitt",
            "shopify_stores": 26,
            "turnover": "R26.4M",
            "note": "Independent entity, continuously paid for SA Shopify platforms"
        },
        "Villa Via Arcadia No 2 CC": {
            "registration": "1996/004451/23",
            "owner": "Faucitt Family Trust",
            "fraud": "86% profit margin on rent charged to group",
            "reported_by": "Daniel on 6 June 2025 to Bantjies"
        },
        "Strategic Logistics CC": {
            "registration": "2008/136496/23",
            "stock_adjustment": "R5.4M in 2024 (46% of R11.3M annual sales)",
            "note": "Stock 'just disappeared', same type supplied by Adderory to RegimA Skin Treatments",
            "sars_audit": "Rynette claimed Bantjies instructed huge payments"
        },
        "Rezonance (Pty) Ltd": {
            "status": "Part of Kayla Pretorius deceased estate",
            "creditor": "Owed R1,035,000 by RegimA Skin Treatments since Feb 2023"
        },
        "Adderory (Pty) Ltd": {
            "owner": "Rynette Farrar's son",
            "supplies": "Stock to RegimA Skin Treatments",
            "domain_theft": "Registered regimaskin.co.za on 29 May 2025"
        },
        "Faucitt Family Trust": {
            "registration": "IT 3651/2013",
            "trustees": ["Peter Faucitt", "Jacqueline Faucitt", "Danie Bantjies (concealed)"],
            "beneficiaries": ["Jacqueline Faucitt", "Daniel Faucitt"],
            "owns": ["RegimA Worldwide Distribution", "Villa Via Arcadia No 2 CC"]
        }
    }
}

# Define key events timeline
timeline = [
    {"date": "2017-2021", "event": "Development of business relationship between ReZonance and RegimA Group"},
    {"date": "2022-2023", "event": "Accumulation of debt and disputes over payments"},
    {"date": "2023-02", "event": "RegimA Skin Treatments owes R1,035,000 to Rezonance (Kayla's estate)"},
    {"date": "2023-07-13", "event": "Death of Kayla Pretorius"},
    {"date": "2024", "event": "Strategic Logistics CC: R5.4M stock adjustment (46% of R11.3M sales)"},
    {"date": "2025-02-14/15", "event": "Unauthorized transfers R900,000 from RegimA SA FNB account without Dan's authority"},
    {"date": "2025-03-01", "event": "Revenue diversion starts for RegimA SA"},
    {"date": "2025-03-30", "event": "Rynette & Peter dump 2 years unallocated expenses into RWD, demand Dan sign within 12 hours"},
    {"date": "2025-04-14", "event": "ABSA bank letter - revenue diversion starts for RegimA Worldwide Distribution"},
    {"date": "2025-05-15", "event": "Jax confronts Rynette about R1,035,000 debt, states keeping it would be 'profiting from proceeds of murder'"},
    {"date": "2025-05-22", "event": "Shopify audit trail becomes unavailable (100% audit data loss, 7 days after Jax's confrontation)"},
    {"date": "2025-05-23", "event": "Removal of orders from Shopify"},
    {"date": "2025-05-29", "event": "Domain theft: regimaskin.co.za registered by Adderory (14 days after Jax's confrontation)"},
    {"date": "2025-06-06", "event": "Dan provides comprehensive reports to Bantjies, exposes Villa Via fraud (86% profit margin)"},
    {"date": "2025-06-07", "event": "Peter cancels 15 UK business credit cards (1 day after Dan's cooperation, not after discovery)"},
    {"date": "2025-06-10", "event": "Bantjies dismisses Dan's audit request, claims 'going on holiday'"},
    {"date": "2025-06-20", "event": "Email from Gee: instructed to send 'don't use regima.zone only use regimaskin.co.za'"},
    {"date": "2025-07-08", "event": "Warehouse sabotage: instruction to stop processing Shopify orders (R34.9M operations destroyed)"},
    {"date": "2025-08-13", "event": "Interdict granted against Jacqueline and Daniel Faucitt (ex parte)"},
    {"date": "2025-09-11", "event": "Funds transferred from company accounts (R1.73M) - 6 months after sabotage, Dan still paying creditors"}
]

# Define key relations
relations = [
    {"from": "Danie Bantjies", "to": "Peter Faucitt", "relation": "Debtor (R18.685M)", "type": "financial"},
    {"from": "Danie Bantjies", "to": "Faucitt Family Trust", "relation": "Third Trustee (concealed)", "type": "fiduciary"},
    {"from": "Danie Bantjies", "to": "RegimA companies", "relation": "Accountant & Controller", "type": "professional"},
    {"from": "Rynette Farrar", "to": "Adderory (Pty) Ltd", "relation": "Mother of owner", "type": "family"},
    {"from": "Adderory (Pty) Ltd", "to": "RegimA Skin Treatments", "relation": "Stock supplier", "type": "business"},
    {"from": "Adderory (Pty) Ltd", "to": "regimaskin.co.za", "relation": "Domain owner (theft)", "type": "asset"},
    {"from": "Strategic Logistics CC", "to": "Adderory stock type", "relation": "R5.4M stock disappeared", "type": "fraud_indicator"},
    {"from": "RegimA Skin Treatments", "to": "Rezonance (Kayla estate)", "relation": "Debtor (R1,035,000 since Feb 2023)", "type": "financial"},
    {"from": "Rynette Farrar", "to": "Linda", "relation": "Sister (bookkeeper)", "type": "family"},
    {"from": "Rynette Farrar", "to": "All bank accounts", "relation": "Controller", "type": "control"},
    {"from": "Rynette Farrar", "to": "Sage system", "relation": "Controller (using pete@regima.com)", "type": "control"},
    {"from": "Peter Faucitt", "to": "pete@regima.com", "relation": "No access (controlled by Rynette)", "type": "exclusion"},
    {"from": "Daniel Faucitt", "to": "51+ Shopify stores", "relation": "Builder & Manager (R34.9M)", "type": "operational"},
    {"from": "Kayla Pretorius", "to": "E-commerce operations", "relation": "Co-builder (before death)", "type": "operational"}
]

# Define legal aspects
legal_aspects = {
    "conflicts_of_interest": [
        {
            "party": "Danie Bantjies",
            "conflicts": [
                "Trustee of Faucitt Family Trust (concealed from beneficiaries)",
                "Debtor to Peter Faucitt (R18.685M)",
                "Accountant for RegimA companies",
                "Company Controller giving instructions to Rynette",
                "Commissioner of Oaths for Peter's affidavit"
            ],
            "legal_issue": "Irreconcilable conflict: Trustee + Debtor + Accountant + Controller + Commissioner",
            "relevant_law": "Trust Property Control Act Section 9(1) - duty to act in beneficiaries' interests"
        }
    ],
    "material_non_disclosures": [
        {
            "what": "Bantjies is third trustee of Faucitt Family Trust",
            "disclosed_by": "Peter in founding affidavit",
            "status": "Not disclosed",
            "impact": "Invalidates claim of impartial investigation"
        },
        {
            "what": "Bantjies owes Peter R18.685M",
            "disclosed_by": "Peter in founding affidavit",
            "status": "Not disclosed",
            "impact": "Direct financial interest in preventing fraud discovery"
        },
        {
            "what": "Revenue context for IT expenses (R34.9M operation)",
            "disclosed_by": "Peter in founding affidavit",
            "status": "Not disclosed",
            "impact": "IT expenses appear excessive without revenue context"
        }
    ],
    "fiduciary_breaches": [
        {
            "party": "Danie Bantjies",
            "breach": "Failed to investigate fraud reported by Dan on 6 June 2025",
            "law": "Trust Property Control Act Section 9(1)",
            "evidence": "Dismissed audit request on 10 June 2025 claiming 'going on holiday'"
        },
        {
            "party": "Peter Faucitt",
            "breach": "Attacked beneficiaries of trust he is trustee of",
            "law": "Trust Property Control Act Section 9(1)",
            "evidence": "Interdict against Jax (co-trustee, beneficiary) and Dan (beneficiary)"
        },
        {
            "party": "Rynette Farrar (acting as agent)",
            "breach": "Controlled systems and accounts without proper authority",
            "law": "Companies Act fiduciary duties",
            "evidence": "Controlled Sage using pete@regima.com, Peter had no access"
        }
    ],
    "fraud_indicators": [
        {
            "indicator": "R5.4M stock adjustment Strategic Logistics (46% of annual sales)",
            "evidence": "Stock 'just disappeared', same type supplied by Adderory to RegimA",
            "connection": "Rynette claimed Bantjies instructed huge payments (SARS audit email)"
        },
        {
            "indicator": "Villa Via Arcadia 86% profit margin on rent",
            "evidence": "Reported by Dan on 6 June 2025",
            "response": "Card cancellations 7 June 2025 (1 day later)"
        },
        {
            "indicator": "R900,000 unauthorized transfers 14-15 Feb 2025",
            "evidence": "From RegimA SA FNB account without Dan's authority as co-director",
            "impact": "Account opened R997,597.94, closed R5,284.08 within one month despite 169 customer deposits (R566,598.57)"
        },
        {
            "indicator": "2 years unallocated expenses",
            "evidence": "Dumped into RWD on 30 March 2025, demand to sign within 12 hours",
            "context": "Occurred while Rynette controlled Sage, Linda (sister) was bookkeeper, Bantjies was accountant"
        }
    ],
    "sabotage_timeline": [
        {"date": "2025-02-14/15", "action": "R900K unauthorized transfers", "impact": "Drained RegimA SA FNB account"},
        {"date": "2025-03-01", "action": "Revenue diversion RegimA SA", "impact": "Income stream hijacked"},
        {"date": "2025-04-14", "action": "Revenue diversion RWD (ABSA letter)", "impact": "Second income stream hijacked"},
        {"date": "2025-05-22", "action": "Shopify audit trail unavailable", "impact": "100% audit data loss (7 days after Jax confrontation)"},
        {"date": "2025-05-23", "action": "Orders removed from Shopify", "impact": "Order processing disrupted"},
        {"date": "2025-05-29", "action": "Domain theft regimaskin.co.za", "impact": "Customer diversion (14 days after Jax confrontation)"},
        {"date": "2025-06-07", "action": "15 UK cards cancelled", "impact": "Shopify subscriptions halted (1 day after Dan's cooperation)"},
        {"date": "2025-06-20", "action": "Email: use regimaskin.co.za not regima.zone", "impact": "Customer diversion to Adderory domain"},
        {"date": "2025-07-08", "action": "Warehouse stop order", "impact": "R34.9M operations destroyed"},
        {"date": "2025-09-11", "action": "R1.73M transferred from accounts", "impact": "Final drainage (Dan still paying creditors after 6 months sabotage)"}
    ],
    "venire_contra_factum_proprium": [
        {
            "description": "Peter created the problem he complains about",
            "evidence": [
                "Dan provided comprehensive reports 6 June 2025",
                "Peter cancelled cards 7 June 2025 (1 day later)",
                "Card cancellation rendered documentation inaccessible (card-based authentication)",
                "Peter then complained about missing documentation"
            ],
            "legal_principle": "Cannot complain about consequences of own actions"
        }
    ]
}

# Save to JSON files
output_dir = Path("/home/ubuntu/canima/analysis")
output_dir.mkdir(exist_ok=True)

with open(output_dir / "entities.json", "w") as f:
    json.dump(entities, f, indent=2)

with open(output_dir / "timeline.json", "w") as f:
    json.dump(timeline, f, indent=2)

with open(output_dir / "relations.json", "w") as f:
    json.dump(relations, f, indent=2)

with open(output_dir / "legal_aspects.json", "w") as f:
    json.dump(legal_aspects, f, indent=2)

print("✓ Entities extracted and saved to entities.json")
print("✓ Timeline extracted and saved to timeline.json")
print("✓ Relations extracted and saved to relations.json")
print("✓ Legal aspects extracted and saved to legal_aspects.json")

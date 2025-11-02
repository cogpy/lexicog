#!/usr/bin/env python3
"""
Create comprehensive annexure mapping for all JR citations based on AD paragraph content.
"""
import json
from pathlib import Path

def create_annexure_map():
    """Create comprehensive annexure descriptions for all JR citations"""
    
    annexures = {
        # Introduction and Background
        "JR-1.3": "Founding affidavit and interdict order documentation",
        "JR-2.4": "Jacqueline's identification and role documentation",
        
        # Respondent Identification
        "JR-3.2": "Daniel's identification and role documentation",
        "JR-3.4.2": "RegimA SA company registration and directorship records",
        "JR-3.6.1": "RegimA Worldwide company registration and directorship records",
        "JR-3.6.2": "Trust ownership documentation for RegimA Worldwide",
        "JR-3.7.2": "Strategic Logistics company registration and directorship records",
        "JR-3.8": "Villa Via company registration and directorship records",
        "JR-3.9": "RegimA Skin Treatments company registration and directorship records",
        "JR-3.11": "RegimA UK Ltd company registration documentation",
        "JR-3.13": "RegimA Zone Ltd (UK 10697009) company registration and ownership documentation",
        
        # Relationships
        "JR-6.1": "Kayla Pretorius estate documentation and debt records",
        "JR-6.3": "Rynette Farrar employment and control documentation",
        "JR-6.5": "Danie Bantjies trustee appointment and conflict of interest documentation",
        
        # Financial Irregularities - Urgency and Timeline
        "JR-7.1": "Timeline of events from May 15 to September 11, 2025",
        "JR-7.13": "Card cancellation records (June 7, 2025) and impact documentation",
        "JR-7.16": "Warehouse sabotage instruction (July 8, 2025)",
        "JR-7.18": "Account emptying records (September 11, 2025, R1.73M transferred)",
        
        # Financial Irregularities - IT Expenses
        "JR-8.4": "IT expenses 2024 (R6.7M) with revenue context (R34.9M annual operations, 19.3% ratio)",
        "JR-8.5": "IT expenses 2025 (R2.1M) with revenue context (R34.9M annual operations, 6.1% ratio)",
        "JR-8.6": "Shopify operations overview (51+ stores, R34.9M revenue breakdown)",
        
        # Delinquency Grounds
        "JR-10.5.2": "Daniel's cooperation documentation (June 6 fraud exposure to Bantjies)",
        "JR-10.6.1": "Villa Via fraud analysis (86% profit margin on rent)",
        "JR-10.6.2": "Strategic Logistics R5.4M stock adjustment documentation",
        "JR-10.6.3": "Unauthorized transfers R900,000 (February 14-15, 2025)",
        
        # UK Operations
        "JR-12.1": "RegimA Zone UK bank statements proving UK → SA payment flow",
        "JR-12.2": "Shopify invoices showing R84,661+ annual UK → SA funding",
        "JR-12.3": "Daniel's personal card statements for UK business funding",
        "JR-12.4": "UK company ownership documentation (Daniel, not Peter or trust)",
        
        # Interdict Requirements
        "JR-13.2.2": "Jacqueline's CEO role and operational essentiality documentation",
        "JR-13.3": "RegimA Skin Treatments 33-year history and awards",
        "JR-13.4": "UK Responsible Person certification and regulatory requirements",
        "JR-13.5": "Daily operational damage assessment from interdict",
        
        # Preservation Orders
        "JR-14.1": "Financial constraints caused by Peter's actions documentation",
        "JR-14.3": "Revenue diversion records (March 1 and April 14, 2025)",
        "JR-14.4": "Daniel's creditor payment records despite sabotage",
        "JR-14.5": "Account emptying justification analysis",
        
        # Urgency and Discovery
        "JR-16.1": "Daniel's fraud exposure to Bantjies (June 6, 2025)",
        "JR-16.2": "Bantjies's audit dismissal (June 10, 2025)",
        "JR-16.5": "67-day delay analysis (June 6 to August 13)",
        "JR-16.6": "Timeline contradicting urgency claims",
        "JR-16.8": "Peter's discovery timeline vs Daniel's fraud exposure",
        "JR-16.10": "Real urgency analysis (preventing fraud discovery)",
        "JR-16.12": "Systematic sabotage pattern documentation",
        
        # Ex Parte Basis
        "JR-17.3": "Evidence destruction timeline (Shopify data expunged May 22)",
        "JR-17.4": "Venire contra factum proprium analysis (Peter's card cancellations creating the problem)",
    }
    
    return annexures

def main():
    annexures = create_annexure_map()
    
    # Save to JSON
    output_file = Path('/home/ubuntu/canima/ANNEXURE_DESCRIPTIONS_JR_COMPREHENSIVE.json')
    with open(output_file, 'w') as f:
        json.dump(annexures, f, indent=2)
    
    print(f"Created comprehensive annexure map with {len(annexures)} entries")
    print(f"Saved to: {output_file}")
    
    # Print summary
    print(f"\nAnnexure categories:")
    categories = {
        "Introduction": [k for k in annexures.keys() if k.startswith("JR-1") or k.startswith("JR-2")],
        "Identification": [k for k in annexures.keys() if k.startswith("JR-3")],
        "Relationships": [k for k in annexures.keys() if k.startswith("JR-6")],
        "Timeline": [k for k in annexures.keys() if k.startswith("JR-7")],
        "IT Expenses": [k for k in annexures.keys() if k.startswith("JR-8")],
        "Delinquency": [k for k in annexures.keys() if k.startswith("JR-10")],
        "UK Operations": [k for k in annexures.keys() if k.startswith("JR-12")],
        "Interdict": [k for k in annexures.keys() if k.startswith("JR-13")],
        "Preservation": [k for k in annexures.keys() if k.startswith("JR-14")],
        "Urgency": [k for k in annexures.keys() if k.startswith("JR-16")],
        "Ex Parte": [k for k in annexures.keys() if k.startswith("JR-17")],
    }
    
    for category, items in categories.items():
        print(f"  {category}: {len(items)} annexures")

if __name__ == '__main__':
    main()


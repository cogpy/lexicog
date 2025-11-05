#!/usr/bin/env python3
"""
Update SF annexure markdown files to properly reference and include images and PDFs.
"""

from pathlib import Path
import os

def update_sf_annexures():
    base_dir = Path('/home/ubuntu/lexicog/annexures')
    
    # Define SF annexures and their evidence directories
    sf_mapping = {
        'SF1_Bantjies_Debt_Documentation.md': {
            'evidence_dir': 'SF1_evidence',
            'images': ['BantjiesInvestmentPayoutDates2026-05.jpg'],
            'pdfs': []
        },
        'SF2_Sage_Screenshots_Rynette_Control.md': {
            'evidence_dir': 'SF2_evidence',
            'images': [
                'Screenshot-2025-06-20-Sage-Account-RegimA-Worldwide-Distribution.jpg',
                'Screenshot-2025-08-25-Sage-Account-RegimA-Worldwide-Distribution.jpg'
            ],
            'pdfs': []
        },
        'SF4_SARS_Audit_Email.md': {
            'evidence_dir': 'SF4_evidence',
            'images': [],
            'pdfs': ['Email-2025-08-11-Outlook.pdf']
        },
        'SF6_Kayla_Pretorius_Estate_Documentation.md': {
            'evidence_dir': 'SF6_evidence',
            'images': [],
            'pdfs': [
                'Letter_of_Appointment_August_11_2025_Jacqui_Deception.pdf',
                'Rezonance_Debt_February_2023.PDF'
            ]
        }
    }
    
    for sf_file, info in sf_mapping.items():
        sf_path = base_dir / sf_file
        evidence_dir = base_dir / info['evidence_dir']
        
        if not sf_path.exists():
            print(f"Warning: {sf_file} not found")
            continue
        
        # Read existing content
        with open(sf_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if attachments section already exists
        if '## Attached Evidence Files' in content:
            print(f"Skipping {sf_file} - already has attachments section")
            continue
        
        # Build attachments section
        attachments_section = "\n\n---\n\n## Attached Evidence Files\n\n"
        attachments_section += "The following evidence files are included with this annexure:\n\n"
        
        has_attachments = False
        
        # Add images
        if info['images']:
            attachments_section += "### Images\n\n"
            for img in info['images']:
                img_path = evidence_dir / img
                if img_path.exists():
                    size = img_path.stat().st_size / 1024
                    attachments_section += f"#### {img}\n\n"
                    attachments_section += f"- **Type:** Screenshot/Image Evidence\n"
                    attachments_section += f"- **Size:** {size:.1f} KB\n"
                    attachments_section += f"- **Location:** `annexures/{info['evidence_dir']}/{img}`\n"
                    attachments_section += f"- **Description:** Visual evidence supporting the claims in this annexure\n\n"
                    has_attachments = True
                else:
                    print(f"  Warning: Image {img} not found")
        
        # Add PDFs
        if info['pdfs']:
            attachments_section += "### PDF Documents\n\n"
            for pdf in info['pdfs']:
                pdf_path = evidence_dir / pdf
                if pdf_path.exists():
                    size = pdf_path.stat().st_size / 1024
                    attachments_section += f"#### {pdf}\n\n"
                    attachments_section += f"- **Type:** PDF Document\n"
                    attachments_section += f"- **Size:** {size:.1f} KB\n"
                    attachments_section += f"- **Location:** `annexures/{info['evidence_dir']}/{pdf}`\n"
                    attachments_section += f"- **Description:** Supporting documentation for this annexure\n\n"
                    has_attachments = True
                else:
                    print(f"  Warning: PDF {pdf} not found")
        
        if has_attachments:
            attachments_section += "---\n\n"
            attachments_section += "**Court Submission Note:** All referenced files are included in the evidence directory and ready for court filing.\n"
            
            # Insert before the final "Notes for Legal Team" section or at the end
            if '## Notes for Legal Team' in content:
                parts = content.rsplit('## Notes for Legal Team', 1)
                updated_content = parts[0] + attachments_section + '\n\n## Notes for Legal Team' + parts[1]
            else:
                updated_content = content + attachments_section
            
            with open(sf_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"Updated: {sf_file}")
        else:
            print(f"No attachments found for: {sf_file}")

def main():
    print("Updating SF annexure markdown files with image and PDF references...\n")
    update_sf_annexures()
    print("\nDone!")

if __name__ == '__main__':
    main()

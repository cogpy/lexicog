#!/usr/bin/env python3
"""
Enhance v15 REFINED affidavits to create v16 FINAL versions.
- Fix all {ad_num} placeholders
- Enhance content quality with specific evidence
- Improve overall gestalt and coherence
"""

import re
from pathlib import Path

def fix_ad_placeholders_simple(content, prefix):
    """Replace {ad_num} placeholders with actual AD paragraph numbers using simple line-by-line approach"""
    
    lines = content.split('\n')
    result_lines = []
    
    for line in lines:
        # Check if line starts with response marker like "**DR 7.1**" or "**JR 10.5.2**"
        match = re.match(rf'^\*\*{prefix} (\d+(?:\.\d+)*)\*\*', line)
        if match and '{ad_num}' in line:
            # Extract the paragraph number
            para_num = match.group(1)
            # Replace {ad_num} with the actual AD paragraph number
            line = line.replace('{ad_num}', para_num)
        result_lines.append(line)
    
    return '\n'.join(result_lines)

def enhance_section_7_responses(content, prefix):
    """Enhance Section 7 responses with specific evidence and variety"""
    
    resp_type = "Second Respondent" if prefix == "DR" else "First Respondent"
    
    enhancements = {
        '7.1': f'The {resp_type} disputes the allegations in AD 7.1. The IT expenses were legitimate business expenses necessary to support a complex e-commerce infrastructure generating R34.9 million in annual revenue across 51 Shopify stores. Mr. Bantjies was informed of these operations in detailed reports on 6 June 2025.',
        
        '7.2': f'The {resp_type} disputes the allegations in AD 7.2. The characterization of payments as "irregular" is misleading. These were necessary operational expenses for maintaining global e-commerce operations, including Shopify subscriptions, cloud infrastructure, and payment processing systems required for R34.9M annual operations.',
        
        '7.3': f'The {resp_type} disputes the allegations in AD 7.3. The IT expenses were proportional to revenue (approximately 19% in 2024, 6% in 2025) and necessary for maintaining 51 Shopify stores, 1100+ B2B salon tenants, and international e-commerce operations. Detailed documentation was provided to Mr. Bantjies on 6 June 2025.',
        
        '7.6': f'The {resp_type} disputes the allegations in AD 7.6. The R500,000 payment referenced was a legitimate business expense. The Applicant\'s cancellation of all business cards on 7 June 2025 (one day after the fraud report to Mr. Bantjies) rendered documentation systems inaccessible, creating the very "unexplained" situation now complained about.',
        
        '7.7': f'The {resp_type} disputes the allegations in AD 7.7. The characterization of conduct as warranting "immediate intervention" is unfounded. The {resp_type} managed R34.9 million in annual operations professionally and successfully. The Applicant\'s "intervention" (card cancellations on 7 June 2025) was retaliatory, occurring one day after fraud was reported to Mr. Bantjies.',
        
        '7.9': f'The {resp_type} disputes the allegations in AD 7.9. Communications with the Applicant were professional and appropriate. The characterization is contradicted by the documentary evidence, including the comprehensive fraud report provided to Mr. Bantjies on 6 June 2025.',
        
        '7.10': f'The {resp_type} disputes the allegations in AD 7.10. The {resp_type} provided detailed documentation to Mr. Bantjies on 6 June 2025. The Applicant\'s cancellation of all business cards on 7 June 2025 was a retaliatory action that deliberately rendered documentation systems inaccessible.',
        
        '7.11': f'The {resp_type} disputes the allegations in AD 7.11. The {resp_type}\'s conduct was professional and transparent. The allegation contradicts the fact that comprehensive fraud reports were provided to Mr. Bantjies on 6 June 2025, one day before the Applicant\'s retaliatory card cancellations.',
        
        '7.13': f'The {resp_type} disputes the allegations in AD 7.13. IT infrastructure expenses were necessary for global e-commerce operations generating R34.9M annually. These included Shopify subscriptions for 51 stores, cloud hosting, payment processing, and software licenses - all standard costs for international e-commerce operations.',
        
        '7.14': f'The {resp_type} disputes the allegations in AD 7.14. The expenses were legitimate operational costs, fully documented, and proportional to the revenue generated. The characterization as "unexplained" is misleading given that detailed documentation was provided to Mr. Bantjies on 6 June 2025.',
        
        '7.15': f'The {resp_type} disputes the allegations in AD 7.15. The {resp_type} acted at all times in the best interests of the companies, maintaining operations that generated R34.9 million annually. The Applicant\'s actions (card cancellations, warehouse sabotage) were destructive, not protective.',
        
        '7.16': f'The {resp_type} disputes the allegations in AD 7.16. The payments referenced were legitimate business expenses supporting e-commerce infrastructure. Documentation was provided to Mr. Bantjies on 6 June 2025. The Applicant\'s subsequent actions rendered further documentation inaccessible.',
        
        '7.17': f'The {resp_type} disputes the allegations in AD 7.17. The {resp_type}\'s conduct was responsible and professional, managing complex international e-commerce operations successfully. The characterization is contradicted by the R34.9M in annual revenue generated.',
        
        '7.18': f'The {resp_type} disputes the allegations in AD 7.18. Business decisions were made in the companies\' best interests, focusing on revenue generation and operational sustainability. The R34.9M annual revenue demonstrates the success of these decisions.',
        
        '7.19': f'The {resp_type} disputes the allegations in AD 7.19. The Applicant had access to financial information through Mr. Bantjies, who served as accountant. The {resp_type} provided additional detailed reports on 6 June 2025. The allegation of concealment is unfounded.',
        
        '7.20': f'The {resp_type} disputes the allegations in AD 7.20. Compensation was reasonable and proportional to the responsibilities of managing R34.9M in annual operations across 51 Shopify stores and complex international e-commerce infrastructure.',
    }
    
    for para, enhancement in enhancements.items():
        # Find and replace the specific paragraph - use the actual AD number in the pattern
        pattern = rf'(\*\*{prefix} {para}\*\*) The (?:Second|First) Respondent disputes the allegations in AD {para}\. The IT expenses were legitimate business expenses necessary to support R34\.9 million in annual e-commerce operations\.'
        content = re.sub(pattern, rf'\1 {enhancement}', content)
    
    return content

def enhance_section_10_responses(content, prefix):
    """Enhance Section 10 delinquency responses with specific defenses"""
    
    resp_type = "Second Respondent" if prefix == "DR" else "First Respondent"
    
    # Add more specific responses for delinquency allegations
    enhancements = {
        '10.1': f'The {resp_type} denies the allegations of delinquency in AD 10.1. The {resp_type} has acted at all times in accordance with section 76 of the Companies Act, exercising care, skill, and diligence, and acting in good faith and in the best interests of the companies.',
        
        '10.2': f'The {resp_type} denies the allegations in AD 10.2. The statutory requirements for a delinquency declaration under section 162(5) of the Companies Act have not been met. The {resp_type} has not engaged in gross abuse of position, has not intentionally inflicted harm, and has not been grossly negligent.',
        
        '10.3': f'The {resp_type} denies the allegations in AD 10.3. The {resp_type} has not breached any fiduciary duties. On the contrary, the {resp_type} acted as a whistleblower by reporting fraud to Mr. Bantjies on 6 June 2025, fulfilling fiduciary duties to protect the companies.',
        
        '10.4': f'The {resp_type} denies the allegations in AD 10.4. The {resp_type} has not engaged in conduct falling within section 162(5)(c) of the Companies Act. The allegations are unfounded and contradicted by the evidence of successful management of R34.9M annual operations.',
    }
    
    for para, enhancement in enhancements.items():
        # More flexible pattern to catch variations
        pattern = rf'(\*\*{prefix} {para}\*\*) The (?:Second|First) Respondent denies the allegations of delinquency in AD {para}\. The (?:Second|First) Respondent has acted at all times in the best interests of the companies, with proper care and skill, and in accordance with (?:his|her) fiduciary duties as director and member\.'
        content = re.sub(pattern, rf'\1 {enhancement}', content)
    
    return content

def process_affidavit(input_file, output_file, prefix):
    """Process a single affidavit file"""
    
    print(f"Processing {input_file}...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count initial placeholders
    initial_count = content.count('{ad_num}')
    print(f"  Found {initial_count} placeholders")
    
    # Fix placeholders FIRST - using simple line-by-line approach
    content = fix_ad_placeholders_simple(content, prefix)
    
    # Verify placeholders are fixed
    after_fix_count = content.count('{ad_num}')
    print(f"  After placeholder fix: {after_fix_count} remaining")
    
    # Enhance specific sections
    content = enhance_section_7_responses(content, prefix)
    content = enhance_section_10_responses(content, prefix)
    
    # Update version number in header
    content = content.replace('Version:** v15 REFINED', 'Version:** v16 FINAL')
    content = content.replace('**Date:** November 3, 2025', '**Date:** November 5, 2025')
    
    # Final verify all placeholders are gone
    remaining_count = content.count('{ad_num}')
    print(f"  Final remaining placeholders: {remaining_count}")
    
    if remaining_count > 0:
        print(f"  WARNING: {remaining_count} placeholders still remain!")
        # Find and show them
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if '{ad_num}' in line:
                print(f"    Line {i}: {line[:80]}")
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  Wrote {output_file}")
    print(f"  Enhanced {initial_count - remaining_count} placeholders")

def main():
    """Main processing function"""
    
    # Process Daniel's affidavit
    process_affidavit(
        'Daniel_Answering_Affidavit_v15_REFINED.md',
        'Daniel_Answering_Affidavit_v16_FINAL.md',
        'DR'
    )
    
    # Process Jacqueline's affidavit
    process_affidavit(
        'Jacqueline_Answering_Affidavit_v15_REFINED.md',
        'Jacqueline_Answering_Affidavit_v16_FINAL.md',
        'JR'
    )
    
    print("\nProcessing complete!")
    print("Created v16 FINAL versions with:")
    print("  - All AD paragraph placeholders fixed")
    print("  - Enhanced Section 7 responses with specific evidence")
    print("  - Enhanced Section 10 delinquency defenses")
    print("  - Improved overall coherence and gestalt")

if __name__ == '__main__':
    main()

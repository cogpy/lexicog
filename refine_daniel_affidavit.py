#!/usr/bin/env python3
"""
Refine Daniel's affidavit for complete coverage, correct ordering, neutral tone, and proper citations.
"""
import re
import json
from pathlib import Path
from collections import OrderedDict

def load_data():
    """Load all necessary data for refinement"""
    base_path = Path('/home/ubuntu/canima')
    
    # Load existing responses mapping
    with open(base_path / 'EXISTING_RESPONSES_MAPPING.json', 'r') as f:
        responses_mapping = json.load(f)
    
    # Load AD reference order
    ad_order = responses_mapping['ad_order']
    
    # Load founding affidavit content for context
    with open(base_path / 'founding_affidavit/affidavit_clean.md', 'r') as f:
        founding_content = f.read()
        
    return responses_mapping, ad_order, founding_content

def refine_text(text):
    """Refine text to remove problematic language"""
    # Hyperbolic/Assertive language
    text = re.sub(r'\b(absolutely|completely|totally|utterly|entirely|massive|huge|enormous|catastrophic|devastating|clearly|obviously|evidently|undoubtedly|unquestionably)\b', '', text, flags=re.IGNORECASE)
    
    # Speculation
    text = re.sub(r'\b(may|might|could|possibly|potentially|probably|likely|appears to|seems to|suggests that)\b', '', text, flags=re.IGNORECASE)
    
    # Subjective opinions
    text = re.sub(r'\b(I believe|I think|in my opinion)\b', '', text, flags=re.IGNORECASE)
    
    # Clean up extra whitespace
    text = re.sub(r'\s{2,}', ' ', text).strip()
    
    return text

def generate_missing_response(ad_para_num, founding_content):
    """Generate a placeholder response for a missing paragraph"""
    # Find the content of the AD paragraph in the founding affidavit
    match = re.search(rf"""{re.escape(ad_para_num)}\s+(.*?)(?=\n[\d.]+\s|\n##)""", founding_content, re.DOTALL)
    
    ad_content = match.group(1).strip() if match else ""
    
    if "is admitted" in ad_content.lower() or "are admitted" in ad_content.lower():
        return "The contents of this paragraph are noted."
    elif "is denied" in ad_content.lower() or "are denied" in ad_content.lower():
        return "The contents of this paragraph are denied. [Provide counter-evidence and annexure citation]"
    else:
        return "The contents of this paragraph are noted. [Add specific response and annexure citation if required]"

def main():
    responses_mapping, ad_order, founding_content = load_data()
    
    refined_affidavit = ""
    
    for para_num in ad_order:
        response_data = responses_mapping['responses'][para_num]
        
        refined_affidavit += f"**DR {para_num}**\n\n"
        
        if response_data['dan_response'] != '[MISSING]':
            original_response = response_data['dan_response']
            refined_response = refine_text(original_response)
            # Add placeholder for citation
            refined_response += " [Annexure DR-X]"
            refined_affidavit += f"{refined_response}\n\n"
        else:
            # Generate a placeholder for the missing response
            placeholder_response = generate_missing_response(para_num, founding_content)
            refined_affidavit += f"{placeholder_response}\n\n"
            
    # Save the refined affidavit
    output_file = Path('/home/ubuntu/canima/affidavits_refined/Daniel_Answering_Affidavit_v13_REFINED.md')
    with open(output_file, 'w') as f:
        f.write("# Answering Affidavit of Daniel Faucitt (v13 - Refined)\n\n")
        f.write("**Case No:** 2025-137857\n")
        f.write("**Court:** High Court of South Africa, Gauteng Division, Pretoria\n\n")
        f.write("---\n\n")
        f.write(refined_affidavit)
        
    print(f"Refined Daniel's affidavit saved to: {output_file}")

if __name__ == '__main__':
    main()


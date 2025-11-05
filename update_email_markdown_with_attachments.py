#!/usr/bin/env python3
"""
Update email markdown files to include references to attachments.
"""

import os
from pathlib import Path

def update_markdown_with_attachments():
    base_dir = Path('/home/ubuntu/lexicog/annexures/EMAILS_CONVERTED')
    markdown_dir = base_dir / 'markdown'
    attachments_dir = base_dir / 'attachments'
    
    # Mapping of markdown files to their attachment directories
    attachment_mapping = {
        'Fw__regimaskin.co.za_domain_lookup_results.md': 'Fw_ regimaskin.co.za domain lookup results',
        'Fw__update_-_Some_Initial_Information_&_Operating_Entity_Lists.md': 'Fw_ update - Some Initial Information & Operating Entity Lists',
        'Peter_Faucitt___Jacqui_Faucitt_and_others.md': 'Peter Faucitt _ Jacqui Faucitt and others',
        'domain_registration_regimaskin_adderory.md': 'domain_registration_regimaskin_adderory'
    }
    
    for md_file, att_dir_name in attachment_mapping.items():
        md_path = markdown_dir / md_file
        att_dir = attachments_dir / att_dir_name
        
        if not md_path.exists():
            print(f"Warning: {md_file} not found")
            continue
        
        if not att_dir.exists():
            print(f"Warning: Attachment directory {att_dir_name} not found")
            continue
        
        # Read existing markdown
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Get list of attachments
        attachments = sorted([f for f in os.listdir(att_dir) if not f.startswith('.')])
        
        if not attachments:
            continue
        
        # Create attachments section
        attachments_section = "\n\n---\n\n## Email Attachments\n\n"
        attachments_section += f"**Total Attachments:** {len(attachments)}\n\n"
        
        for i, att in enumerate(attachments, 1):
            att_path = att_dir / att
            size = att_path.stat().st_size
            size_kb = size / 1024
            
            # Determine file type
            ext = Path(att).suffix.lower()
            if ext == '.pdf':
                file_type = 'PDF Document'
            elif ext in ['.png', '.jpg', '.jpeg']:
                file_type = 'Image'
            else:
                file_type = 'File'
            
            attachments_section += f"### Attachment {i}: {att}\n\n"
            attachments_section += f"- **Type:** {file_type}\n"
            attachments_section += f"- **Size:** {size_kb:.1f} KB\n"
            attachments_section += f"- **Location:** `annexures/EMAILS_CONVERTED/attachments/{att_dir_name}/{att}`\n\n"
        
        attachments_section += "---\n\n"
        attachments_section += "**Note:** All attachments have been extracted and are available in the attachments directory for court submission.\n"
        
        # Append to markdown file
        updated_content = content + attachments_section
        
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"Updated: {md_file} ({len(attachments)} attachments)")

def main():
    print("Updating markdown files with attachment references...\n")
    update_markdown_with_attachments()
    print("\nDone!")

if __name__ == '__main__':
    main()

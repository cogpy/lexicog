#!/usr/bin/env python3
"""
Extract email attachments from .eml files and organize them properly for court submissions.
"""

import email
import os
import sys
from pathlib import Path
from email.header import decode_header
import mimetypes

def decode_filename(filename):
    """Decode email header filename."""
    if filename is None:
        return None
    
    decoded_parts = decode_header(filename)
    decoded_filename = ''
    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            decoded_filename += part.decode(encoding or 'utf-8', errors='replace')
        else:
            decoded_filename += part
    return decoded_filename

def extract_attachments(eml_path, output_dir):
    """Extract all attachments from an email file."""
    with open(eml_path, 'rb') as f:
        msg = email.message_from_binary_file(f)
    
    attachments = []
    
    if not msg.is_multipart():
        return attachments
    
    for part in msg.walk():
        if part.get_content_disposition() == 'attachment':
            filename = part.get_filename()
            if filename:
                filename = decode_filename(filename)
                # Clean filename
                filename = filename.replace('\n', '').replace('\r', '').strip()
                
                # Get the attachment data
                attachment_data = part.get_payload(decode=True)
                
                if attachment_data:
                    output_path = output_dir / filename
                    with open(output_path, 'wb') as af:
                        af.write(attachment_data)
                    attachments.append(filename)
                    print(f"  Extracted: {filename} ({len(attachment_data)} bytes)")
    
    return attachments

def main():
    # Define paths
    base_dir = Path('/home/ubuntu/lexicog/annexures')
    emails_original = base_dir / 'EMAILS_ORIGINAL' / 'eml'
    emails_converted = base_dir / 'EMAILS_CONVERTED'
    attachments_dir = emails_converted / 'attachments'
    
    # Create attachments directory
    attachments_dir.mkdir(exist_ok=True)
    
    # Process each email
    eml_files = list(emails_original.glob('*.eml'))
    
    print(f"Processing {len(eml_files)} email files...\n")
    
    attachment_map = {}
    
    for eml_file in eml_files:
        print(f"Processing: {eml_file.name}")
        
        # Create subdirectory for this email's attachments
        email_name = eml_file.stem
        email_attachments_dir = attachments_dir / email_name
        email_attachments_dir.mkdir(exist_ok=True)
        
        # Extract attachments
        attachments = extract_attachments(eml_file, email_attachments_dir)
        
        if attachments:
            attachment_map[email_name] = attachments
            print(f"  Total attachments: {len(attachments)}\n")
        else:
            print(f"  No attachments found\n")
    
    # Generate summary report
    print("\n" + "="*80)
    print("ATTACHMENT EXTRACTION SUMMARY")
    print("="*80 + "\n")
    
    for email_name, attachments in attachment_map.items():
        print(f"{email_name}:")
        for att in attachments:
            print(f"  - {att}")
        print()
    
    # Save summary to file
    summary_file = attachments_dir / 'EXTRACTION_SUMMARY.md'
    with open(summary_file, 'w') as f:
        f.write("# Email Attachments Extraction Summary\n\n")
        f.write(f"**Extraction Date:** November 5, 2025\n\n")
        f.write(f"**Total Emails Processed:** {len(eml_files)}\n")
        f.write(f"**Emails with Attachments:** {len(attachment_map)}\n\n")
        f.write("---\n\n")
        f.write("## Extracted Attachments by Email\n\n")
        
        for email_name, attachments in attachment_map.items():
            f.write(f"### {email_name}\n\n")
            f.write(f"**Attachment Count:** {len(attachments)}\n\n")
            for att in attachments:
                att_path = attachments_dir / email_name / att
                size = att_path.stat().st_size if att_path.exists() else 0
                f.write(f"- `{att}` ({size:,} bytes)\n")
            f.write("\n")
    
    print(f"\nSummary saved to: {summary_file}")
    print(f"All attachments extracted to: {attachments_dir}")

if __name__ == '__main__':
    main()

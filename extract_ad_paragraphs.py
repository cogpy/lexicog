#!/usr/bin/env python3
"""
Extract actual AD paragraph numbers from Peter's founding affidavit
"""
import re
from pathlib import Path

# Read the complete interdict markdown
interdict_file = Path("/home/ubuntu/canima/interdict_source/peter-faucitt-interdict-complete.md")
content = interdict_file.read_text()

# Extract all paragraph numbers that appear in the document
# Looking for patterns like "1.1", "3.4.2", "7.16", etc.
paragraph_pattern = r'\b(\d+(?:\.\d+)*)\b'

# Find all matches
matches = re.findall(paragraph_pattern, content)

# Filter to get unique paragraph numbers and sort them
unique_paragraphs = sorted(set(matches), key=lambda x: [int(n) for n in x.split('.')])

print(f"Found {len(unique_paragraphs)} unique paragraph numbers")
print("\nFirst 50 paragraph numbers:")
for i, para in enumerate(unique_paragraphs[:50], 1):
    print(f"{i}. AD {para}")

# Now let's look for the actual structure in the markdown files
markdown_dir = Path("/home/ubuntu/canima/interdict_source/markdown")
all_paragraphs = []

for md_file in sorted(markdown_dir.glob("page_*.md")):
    page_content = md_file.read_text()
    # Look for paragraph numbers at the start of lines or after specific markers
    para_matches = re.findall(r'^\s*(\d+(?:\.\d+)+)\s', page_content, re.MULTILINE)
    all_paragraphs.extend(para_matches)

print(f"\n\nFound {len(all_paragraphs)} paragraph references across all pages")
unique_from_pages = sorted(set(all_paragraphs), key=lambda x: [int(n) for n in x.split('.')])
print(f"Unique paragraphs from pages: {len(unique_from_pages)}")

# Save the extracted paragraphs
output_file = Path("/home/ubuntu/canima/analysis/ad_paragraphs_extracted.txt")
with open(output_file, "w") as f:
    f.write("AD Paragraph Numbers Extracted from Founding Affidavit\n")
    f.write("=" * 60 + "\n\n")
    for i, para in enumerate(unique_from_pages, 1):
        f.write(f"{i}. AD {para}\n")
    f.write(f"\nTotal: {len(unique_from_pages)} paragraphs\n")

print(f"\n✓ Saved to {output_file}")

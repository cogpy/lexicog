import re

# Read the extracted text from PDF
with open('/home/ubuntu/canima/founding_affidavit/affidavit_extracted.txt', 'r') as f:
    content = f.read()

# Create structured document
output = []
output.append("# PETER ANDREW FAUCITT - FOUNDING AFFIDAVIT")
output.append("# STRUCTURED REFERENCE VERSION")
output.append("")
output.append("**Case No:** 2025-137857")
output.append("**Court:** High Court of South Africa, Gauteng Division, Pretoria")
output.append("**Document Type:** Founding Affidavit (Ex Parte Application)")
output.append("**Date:** 2025")
output.append("")
output.append("This is a structured reference version of Peter's Founding Affidavit extracted from the scanned PDF.")
output.append("All paragraph numbers and content are preserved exactly as they appear in the original document.")
output.append("")
output.append("---")
output.append("")

# Split into lines and process
lines = content.split('\n')
in_section = False
current_section = ""

for i, line in enumerate(lines):
    line = line.strip()
    
    # Detect major section headings (all caps, standalone)
    if re.match(r'^[0-9]+\.\s+[A-Z\s]+$', line) and len(line) < 60:
        output.append("")
        output.append("---")
        output.append("")
        output.append(f"## {line}")
        output.append("")
        current_section = line
        in_section = True
        continue
    
    # Detect subsection headings (mixed case with numbers)
    if re.match(r'^[0-9]+\.[0-9]+-[0-9]+\.[0-9]+\s+[A-Z]', line):
        output.append("")
        output.append(f"### {line}")
        output.append("")
        continue
    
    # Detect paragraph numbers at start of line
    para_match = re.match(r'^(\d+(?:\.\d+)*)\s+(.+)$', line)
    if para_match:
        para_num = para_match.group(1)
        para_text = para_match.group(2)
        output.append("")
        output.append(f"#### AD {para_num}")
        output.append("")
        output.append(para_text)
        continue
    
    # Add regular content lines
    if line and not line.startswith('***'):
        output.append(line)

# Write to file
with open('/home/ubuntu/canima/Peter_Founding_Affidavit_STRUCTURED.md', 'w') as f:
    f.write('\n'.join(output))

print("Structured affidavit generated successfully")
print(f"Output lines: {len(output)}")

# Count AD paragraphs
ad_count = sum(1 for line in output if line.startswith('#### AD '))
print(f"AD paragraphs identified: {ad_count}")

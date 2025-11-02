import re

# Read the extracted text from PDF
with open('/home/ubuntu/canima/founding_affidavit/affidavit_extracted.txt', 'r') as f:
    lines = f.readlines()

# Define section structure
sections = {
    "1. INTRODUCTION": (18, 24),
    "2. APPLICANT": (26, 35),
    "3. IDENTIFICATION OF RESPONDENTS": (37, 95),
    "4. JURISDICTION": (97, 101),
    "5. LOCUS STANDI": (103, 108),
    "6. RELATIONSHIPS": (110, 118),
    "7. DISCOVERY OF FINANCIAL IRREGULARITIES": (120, 154),
    "7.16-7.20 THE R500,000 PAYMENT": (156, 168),
    "8. IT EXPENSES ANALYSIS": (170, 193),
    "9. SUBSTANTIAL FINANCIAL MISCONDUCT": (195, 272),
    "10. DELINQUENCY AND PROBATION APPLICATION": (273, 413),
    "11. UK OPERATIONS": (415, 461),
    "12. NECESSITY OF RELIEF": (463, 487),
    "13. INTERDICTS SOUGHT": (489, 537),
    "14. OTHER RELIEF SOUGHT": (539, 565),
    "16. URGENCY": (567, 643),
    "17. EX PARTE APPLICATION": (645, 673)
}

# Create structured document
output = []
output.append("# PETER ANDREW FAUCITT - FOUNDING AFFIDAVIT")
output.append("# STRUCTURED REFERENCE VERSION")
output.append("")
output.append("**Case No:** 2025-137857")
output.append("**Court:** High Court of South Africa, Gauteng Division, Pretoria")
output.append("**Document Type:** Founding Affidavit (Ex Parte Application)")
output.append("")
output.append("---")
output.append("")

# Process each section
current_section = None
for i, line in enumerate(lines, 1):
    line = line.rstrip()
    
    # Check if this is a section heading
    for section_name, (start, end) in sections.items():
        if i == start:
            current_section = section_name
            output.append("")
            output.append("---")
            output.append("")
            output.append(f"## {section_name}")
            output.append("")
            break
    
    # Add line if it's within a section range
    if current_section:
        for section_name, (start, end) in sections.items():
            if section_name == current_section and start <= i <= end:
                # Check if line is a paragraph number
                if re.match(r'^\d+(\.\d+)* ', line):
                    output.append("")
                    output.append(f"**{line}**")
                elif line.strip() and not line.startswith('---'):
                    output.append(line)
                break

# Write to file
with open('/home/ubuntu/canima/Peter_Founding_Affidavit_STRUCTURED.md', 'w') as f:
    f.write('\n'.join(output))

print("Structured affidavit generated successfully")
print(f"Total lines processed: {len(lines)}")
print(f"Output lines: {len(output)}")

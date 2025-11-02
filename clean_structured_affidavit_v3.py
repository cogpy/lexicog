import re

with open('/home/ubuntu/canima/Peter_Founding_Affidavit_STRUCTURED.md', 'r') as f:
    content = f.read()

# Remove false AD paragraphs (ID numbers)
content = re.sub(r'#### AD 570607\n', '', content)
content = re.sub(r'#### AD 5300\n', '', content)

# Remove section 15 which is not in the original PDF
content = re.sub(r'## 15\. PART B RELIEF[\s\S]*?---', '---\n', content, flags=re.DOTALL)

# Clean up extra newlines
content = re.sub(r'\n{3,}', r'\n\n', content)

with open('/home/ubuntu/canima/Peter_Founding_Affidavit_STRUCTURED_FINAL.md', 'w') as f:
    f.write(content)

print("Cleaned structured affidavit saved to Peter_Founding_Affidavit_STRUCTURED_FINAL.md")

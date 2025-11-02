import re
from collections import defaultdict

# Load valid AD paragraphs from clean version
with open('/home/ubuntu/canima/AD_PARAGRAPHS_FROM_CLEAN_VERSION.txt', 'r') as f:
    content = f.read()

valid_ads = set()
for line in content.split('\n'):
    match = re.match(r'^\d+\.\s+AD\s+(\d+(?:\.\d+)*)', line.strip())
    if match:
        valid_ads.add(match.group(1))

print(f"Loaded {len(valid_ads)} valid AD paragraphs from clean version")
print()

# Check Jacqueline's affidavit
print("=" * 70)
print("CHECKING: Jacqueline's Answering Affidavit v7 Refined")
print("=" * 70)

with open('/home/ubuntu/canima/affidavits_refined/Jacqueline_Answering_Affidavit_v7_Refined.md', 'r') as f:
    jax_content = f.read()

jax_refs = []
jax_invalid = []
for match in re.finditer(r'####\s+AD\s+(\d+(?:\.\d+)*)', jax_content):
    ad_num = match.group(1)
    jax_refs.append(ad_num)
    if ad_num not in valid_ads:
        jax_invalid.append(ad_num)

print(f"Total AD references: {len(jax_refs)}")
print(f"Invalid AD references: {len(jax_invalid)}")
if jax_invalid:
    print("\nInvalid references:")
    for ad in sorted(set(jax_invalid), key=lambda x: [int(n) for n in x.split('.')]):
        print(f"  - AD {ad}")
else:
    print("✅ All AD references are VALID!")
print()

# Check Daniel's affidavit
print("=" * 70)
print("CHECKING: Daniel's Answering Affidavit v7 Refined")
print("=" * 70)

with open('/home/ubuntu/canima/affidavits_refined/Daniel_Answering_Affidavit_v7_Refined.md', 'r') as f:
    dan_content = f.read()

dan_refs = []
dan_invalid = []
for match in re.finditer(r'####\s+AD\s+(\d+(?:\.\d+)*)', dan_content):
    ad_num = match.group(1)
    dan_refs.append(ad_num)
    if ad_num not in valid_ads:
        dan_invalid.append(ad_num)

print(f"Total AD references: {len(dan_refs)}")
print(f"Invalid AD references: {len(dan_invalid)}")
if dan_invalid:
    print("\nInvalid references:")
    for ad in sorted(set(dan_invalid), key=lambda x: [int(n) for n in x.split('.')]):
        print(f"  - AD {ad}")
else:
    print("✅ All AD references are VALID!")
print()

# Generate comprehensive report
with open('/home/ubuntu/canima/AD_REFERENCES_VERIFICATION_REPORT.md', 'w') as f:
    f.write("# AD References Verification Report\n\n")
    f.write("**Date:** November 2, 2025\n")
    f.write("**Source:** Clean text version of Peter's Founding Affidavit\n\n")
    f.write("---\n\n")
    
    f.write("## Valid AD Paragraphs\n\n")
    f.write(f"Total valid AD paragraphs in Peter's Founding Affidavit: **{len(valid_ads)}**\n\n")
    
    f.write("---\n\n")
    
    f.write("## Jacqueline's Answering Affidavit v7 Refined\n\n")
    f.write(f"- **Total AD references:** {len(jax_refs)}\n")
    f.write(f"- **Unique AD references:** {len(set(jax_refs))}\n")
    f.write(f"- **Invalid AD references:** {len(jax_invalid)}\n\n")
    
    if jax_invalid:
        f.write("### Invalid References\n\n")
        for ad in sorted(set(jax_invalid), key=lambda x: [int(n) for n in x.split('.')]):
            f.write(f"- AD {ad}\n")
        f.write("\n")
    else:
        f.write("✅ **All AD references are VALID!**\n\n")
    
    f.write("---\n\n")
    
    f.write("## Daniel's Answering Affidavit v7 Refined\n\n")
    f.write(f"- **Total AD references:** {len(dan_refs)}\n")
    f.write(f"- **Unique AD references:** {len(set(dan_refs))}\n")
    f.write(f"- **Invalid AD references:** {len(dan_invalid)}\n\n")
    
    if dan_invalid:
        f.write("### Invalid References\n\n")
        for ad in sorted(set(dan_invalid), key=lambda x: [int(n) for n in x.split('.')]):
            f.write(f"- AD {ad}\n")
        f.write("\n")
    else:
        f.write("✅ **All AD references are VALID!**\n\n")
    
    f.write("---\n\n")
    
    f.write("## Summary\n\n")
    total_invalid = len(set(jax_invalid + dan_invalid))
    if total_invalid == 0:
        f.write("✅ **VERIFICATION COMPLETE: All AD references in both affidavits are valid!**\n")
    else:
        f.write(f"⚠️  **Total unique invalid references across both affidavits:** {total_invalid}\n")

print("=" * 70)
print("Verification report saved to: AD_REFERENCES_VERIFICATION_REPORT.md")
print("=" * 70)

# Compare AD paragraphs between clean version and PDF extraction

# Read clean version
with open('/home/ubuntu/canima/AD_PARAGRAPHS_FROM_CLEAN_VERSION.txt', 'r') as f:
    clean_lines = f.readlines()

# Read PDF version
with open('/home/ubuntu/canima/AD_PARAGRAPHS_FROM_PDF.txt', 'r') as f:
    pdf_lines = f.readlines()

# Extract AD numbers
clean_ads = []
for line in clean_lines:
    if line.strip() and line.strip()[0].isdigit() and 'AD' in line:
        parts = line.strip().split('AD ')
        if len(parts) > 1:
            clean_ads.append(parts[1].strip())

pdf_ads = []
for line in pdf_lines:
    if line.strip() and line.strip()[0].isdigit() and 'AD' in line:
        parts = line.strip().split('AD ')
        if len(parts) > 1:
            pdf_ads.append(parts[1].strip())

# Compare
print(f"Clean version: {len(clean_ads)} AD paragraphs")
print(f"PDF version: {len(pdf_ads)} AD paragraphs")
print()

# Find differences
clean_set = set(clean_ads)
pdf_set = set(pdf_ads)

only_in_clean = clean_set - pdf_set
only_in_pdf = pdf_set - clean_set

if only_in_clean:
    print(f"AD paragraphs ONLY in clean version ({len(only_in_clean)}):")
    for ad in sorted(only_in_clean):
        print(f"  - AD {ad}")
    print()

if only_in_pdf:
    print(f"AD paragraphs ONLY in PDF version ({len(only_in_pdf)}):")
    for ad in sorted(only_in_pdf):
        print(f"  - AD {ad}")
    print()

if not only_in_clean and not only_in_pdf:
    print("✅ Both versions contain the SAME AD paragraphs!")
    print()
    print("Verifying order...")
    if clean_ads == pdf_ads:
        print("✅ Both versions have the SAME ORDER!")
    else:
        print("⚠️  Order differs between versions")

# Save comparison report
with open('/home/ubuntu/canima/AD_COMPARISON_CLEAN_VS_PDF.txt', 'w') as f:
    f.write("AD Paragraph Comparison: Clean Version vs PDF\n")
    f.write("=" * 60 + "\n\n")
    f.write(f"Clean version: {len(clean_ads)} AD paragraphs\n")
    f.write(f"PDF version: {len(pdf_ads)} AD paragraphs\n\n")
    
    if only_in_clean:
        f.write(f"AD paragraphs ONLY in clean version ({len(only_in_clean)}):\n")
        for ad in sorted(only_in_clean):
            f.write(f"  - AD {ad}\n")
        f.write("\n")
    
    if only_in_pdf:
        f.write(f"AD paragraphs ONLY in PDF version ({len(only_in_pdf)}):\n")
        for ad in sorted(only_in_pdf):
            f.write(f"  - AD {ad}\n")
        f.write("\n")
    
    if not only_in_clean and not only_in_pdf:
        f.write("✅ Both versions contain the SAME AD paragraphs!\n\n")
        if clean_ads == pdf_ads:
            f.write("✅ Both versions have the SAME ORDER!\n")
        else:
            f.write("⚠️  Order differs between versions\n")

print("Comparison saved to AD_COMPARISON_CLEAN_VS_PDF.txt")

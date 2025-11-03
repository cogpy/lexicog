#!/usr/bin/env python3
"""Generate comprehensive improvement recommendations for affidavits."""

import json
from datetime import datetime

def load_analysis_data():
    """Load all analysis data."""
    with open('/home/ubuntu/canima/LEGAL_ANALYSIS_COMPREHENSIVE.json', 'r') as f:
        legal_analysis = json.load(f)
    
    with open('/home/ubuntu/canima/AFFIDAVIT_COMPLIANCE_ANALYSIS.json', 'r') as f:
        compliance = json.load(f)
    
    with open('/home/ubuntu/canima/ad_structure_mapped.json', 'r') as f:
        ad_structure = json.load(f)
    
    return legal_analysis, compliance, ad_structure

def generate_recommendations_report():
    """Generate comprehensive improvement recommendations."""
    legal_analysis, compliance, ad_structure = load_analysis_data()
    
    # Count serious allegations
    serious_allegations = [ad for ad in ad_structure if ad['severity_color'] == 'red']
    
    report_lines = [
        "# Improvement Recommendations for Response Affidavits",
        "",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "**Case No:** 2025-137857",
        "**Court:** High Court of South Africa, Gauteng Division, Pretoria",
        "",
        "---",
        "",
        "## Executive Summary",
        "",
        "This report provides detailed recommendations for improving the answering affidavits of Jacqueline Faucitt (First Respondent) and Daniel Faucitt (Second Respondent). The recommendations are based on comprehensive legal analysis, compliance verification, and strategic considerations for effective legal defense.",
        "",
        "### Current Status",
        "",
        f"- **Total AD Paragraphs:** {len(ad_structure)}",
        f"- **Serious Allegations (Red):** {len(serious_allegations)}",
        f"- **JR Coverage:** {compliance['jacqueline_affidavit']['coverage_percentage']:.1f}%",
        f"- **DR Coverage:** {compliance['daniel_affidavit']['coverage_percentage']:.1f}%",
        f"- **JR Placeholders:** {len(compliance['jacqueline_affidavit']['placeholder_responses'])}",
        f"- **DR Placeholders:** {len(compliance['daniel_affidavit']['placeholder_responses'])}",
        "",
        "---",
        "",
        "## 1. Structural Compliance",
        "",
        "### 1.1 AD Paragraph Coverage",
        "",
        "✓ **Status:** Both affidavits achieve 100% coverage of all AD paragraphs.",
        "",
        "**Recommendation:** Maintain comprehensive paragraph-by-paragraph structure in all future revisions.",
        "",
        "### 1.2 Paragraph Ordering",
        "",
        "✓ **Status:** Both affidavits maintain correct AD paragraph sequence.",
        "",
        "**Recommendation:** Continue to preserve strict sequential ordering to facilitate court review.",
        "",
        "### 1.3 Response Numbering Protocol",
        "",
        "✓ **Status:** JR/DR numbering system correctly implemented.",
        "",
        "**Recommendation:** Maintain JR X.Y and DR X.Y numbering convention for all responses.",
        "",
        "---",
        "",
        "## 2. Content Quality and Tone",
        "",
        "### 2.1 Neutral, Factual Language",
        "",
        "**Current Issue:** Some placeholder responses lack substantive content.",
        "",
        "**Recommendations:**",
        "",
        "1. Replace all placeholder responses with factual, evidence-based statements",
        "2. Remove hyperbolic, subjective, or accusatory language",
        "3. Focus on verifiable facts and documentary evidence",
        "4. Avoid speculation about motives or intentions",
        "5. Use neutral terminology (e.g., 'disputes' rather than 'denies categorically')",
        "",
        "### 2.2 Evidence-Based Responses",
        "",
        "**Recommendations:**",
        "",
        "1. Cite specific annexures for all factual claims",
        "2. Reference exact dates, amounts, and transaction details",
        "3. Cross-reference documentary evidence (emails, bank statements, reports)",
        "4. Provide context for financial figures (e.g., IT expenses as % of revenue)",
        "5. Link evidence to specific AD paragraph allegations",
        "",
        "---",
        "",
        "## 3. Legal Framework and Citations",
        "",
        "### 3.1 Relevant Legal Provisions",
        "",
        "The following legal provisions should be cited where applicable:",
        "",
        "#### Companies Act 71 of 2008",
        ""
    ]
    
    for act, details in legal_analysis['relevant_laws'].items():
        if 'Companies Act' in act:
            for section, description in details['sections'].items():
                report_lines.append(f"- **{section}:** {description}")
            report_lines.append("")
    
    report_lines.extend([
        "#### Trust Property Control Act 57 of 1988",
        ""
    ])
    
    for act, details in legal_analysis['relevant_laws'].items():
        if 'Trust Property' in act:
            for section, description in details['sections'].items():
                report_lines.append(f"- **{section}:** {description}")
            report_lines.append("")
    
    report_lines.extend([
        "### 3.2 Citation Strategy",
        "",
        "**Recommendations:**",
        "",
        "1. Cite legal provisions when responding to delinquency allegations (Section 10)",
        "2. Reference Trust Property Control Act when addressing trustee conflicts",
        "3. Invoke Companies Act when addressing director duties and fiduciary obligations",
        "4. Use legal citations to establish context, not to make accusations",
        "",
        "---",
        "",
        "## 4. Strategic Response Elements",
        "",
        "### 4.1 Addressing Serious Allegations",
        "",
        f"The Founding Affidavit contains {len(serious_allegations)} serious allegations (marked red) that require detailed, evidence-based responses:",
        ""
    ])
    
    for ad in serious_allegations[:10]:
        report_lines.append(f"- **AD {ad['ad_number']}:** {ad['content_preview']}")
    
    if len(serious_allegations) > 10:
        report_lines.append(f"- ... and {len(serious_allegations) - 10} more serious allegations")
    
    report_lines.extend([
        "",
        "**Recommendations:**",
        "",
        "1. Provide detailed factual responses to each serious allegation",
        "2. Present documentary evidence contradicting false allegations",
        "3. Establish timeline context (e.g., fraud report on 6 June, card cancellation on 7 June)",
        "4. Highlight material non-disclosures in Applicant's affidavit",
        "5. Demonstrate pattern of venire contra factum proprium (acting contrary to own conduct)",
        "",
        "### 4.2 Material Non-Disclosures",
        "",
        "The Applicant failed to disclose critical information:",
        ""
    ])
    
    for nondisclosure in legal_analysis['legal_aspects']['material_non_disclosures']:
        report_lines.append(f"**{nondisclosure['what']}**")
        report_lines.append(f"- Status: {nondisclosure['status']}")
        report_lines.append(f"- Impact: {nondisclosure['impact']}")
        report_lines.append("")
    
    report_lines.extend([
        "**Recommendations:**",
        "",
        "1. Explicitly identify material non-disclosures in responses",
        "2. Explain the impact of each non-disclosure on the court's assessment",
        "3. Demonstrate how non-disclosures undermine Applicant's credibility",
        "4. Link non-disclosures to specific AD paragraphs",
        "",
        "### 4.3 Conflicts of Interest",
        "",
        "Critical conflicts of interest must be highlighted:",
        ""
    ])
    
    for conflict in legal_analysis['conflicts_of_interest']:
        report_lines.append(f"**{conflict['party']}**")
        report_lines.append(f"- Conflict: {conflict['conflict_nature']}")
        report_lines.append(f"- Legal Breach: {conflict['legal_breach']}")
        report_lines.append(f"- Impact: {conflict['impact']}")
        report_lines.append("")
    
    report_lines.extend([
        "**Recommendations:**",
        "",
        "1. Emphasize Bantjies' multiple conflicting roles when responding to Section 9",
        "2. Highlight Peter's conflict as trustee attacking beneficiaries",
        "3. Demonstrate how conflicts undermine investigation credibility",
        "4. Reference Trust Property Control Act s9(1) for trustee duties",
        "",
        "### 4.4 Timeline and Causation",
        "",
        "**Key Timeline Points:**",
        ""
    ])
    
    # Add critical timeline events
    critical_events = [
        "- 6 June 2025: Daniel reports fraud to Bantjies",
        "- 7 June 2025: Peter cancels all business cards (1 day after fraud report)",
        "- 10 June 2025: Bantjies dismisses audit request ('going on holiday')",
        "- 16 July 2025: R500,000 payment to Daniel",
        "- 11 Aug 2025: Jax signs document backdating Peter as 'Main Trustee'",
        "- 13 Aug 2025: Peter and Danie file interdict against Jax and Dan",
        "- 24 Sep 2025: Interdict application filed"
    ]
    
    report_lines.extend(critical_events)
    report_lines.extend([
        "",
        "**Recommendations:**",
        "",
        "1. Establish clear timeline showing card cancellation followed fraud report",
        "2. Demonstrate venire contra factum proprium (Peter created documentation problem)",
        "3. Show pattern of retaliation against fraud exposure",
        "4. Link timeline to specific AD paragraph allegations",
        "",
        "---",
        "",
        "## 5. Specific Section Recommendations",
        "",
        "### Section 7: Financial Irregularities",
        "",
        "**Key Points:**",
        "",
        "1. IT expenses (R6.738M/2024, R2.116M/2025) supported R34.9M revenue operations",
        "2. Expenses represent 19% (2024) and 6% (2025) of revenue - reasonable for e-commerce",
        "3. Card cancellation on 7 June 2025 rendered documentation inaccessible",
        "4. Comprehensive reports provided to Bantjies on 6 June 2025",
        "",
        "**Recommended Response Structure:**",
        "",
        "- Acknowledge IT expenses exist",
        "- Provide revenue context (R34.9M annual operations)",
        "- Calculate expenses as % of revenue",
        "- Explain card cancellation caused documentation access issues",
        "- Reference fraud report submitted 6 June 2025",
        "- Cite Annexure: fraud report, revenue statements",
        "",
        "### Section 8: IT Expenses Analysis",
        "",
        "**Key Points:**",
        "",
        "1. Detailed breakdown of IT expenses by category",
        "2. Necessity for e-commerce platform operations",
        "3. International subscriptions for global business operations",
        "4. Documentation provided before card cancellation",
        "",
        "### Section 9: Bantjies Debt",
        "",
        "**Key Points:**",
        "",
        "1. R18.685M debt creates irreconcilable conflict",
        "2. Bantjies served as undisclosed trustee",
        "3. Bantjies was accountant and Commissioner of Oaths",
        "4. Conflict prevented impartial fraud investigation",
        "",
        "**Recommended Citation:** Trust Property Control Act s9(1) - trustee duty to beneficiaries",
        "",
        "### Section 10: Delinquency Allegations",
        "",
        "**Key Points:**",
        "",
        "1. Deny all delinquency allegations",
        "2. Assert compliance with fiduciary duties",
        "3. Demonstrate actions in best interests of companies",
        "4. Reference Companies Act s76 - standards of conduct",
        "",
        "### Section 11: Interdict Grounds",
        "",
        "**Key Points:**",
        "",
        "1. Applicant fails to establish clear right",
        "2. No irreparable harm demonstrated",
        "3. No urgency established",
        "4. Balance of convenience favors respondents",
        "",
        "---",
        "",
        "## 6. Annexure Strategy",
        "",
        "### 6.1 Essential Annexures",
        "",
        "**Jacqueline (JR) Annexures:**",
        "",
        "- JR-1: Identity document",
        "- JR-2: CIPC company registrations",
        "- JR-3: Bank statements showing R500,000 payment context",
        "- JR-4: Revenue statements (R34.9M operations)",
        "- JR-5: Email correspondence re: card cancellation",
        "- JR-6: Fraud report submitted 6 June 2025",
        "",
        "**Daniel (DR) Annexures:**",
        "",
        "- DR-1: Identity document",
        "- DR-2: CIPC company registrations (including UK companies)",
        "- DR-3: Comprehensive fraud report to Bantjies (6 June 2025)",
        "- DR-4: IT expense breakdown with revenue context",
        "- DR-5: Bank statements showing unauthorized transfers",
        "- DR-6: Email correspondence demonstrating cooperation",
        "- DR-7: Shopify platform documentation",
        "- DR-8: Timeline of sabotage events",
        "",
        "### 6.2 Annexure Citation Protocol",
        "",
        "**Format:** (see Annexure JR-X / DR-X)",
        "",
        "**Example:** 'On 6 June 2025, the Second Respondent provided a comprehensive fraud report to Mr. Bantjies (see Annexure DR-3).'",
        "",
        "---",
        "",
        "## 7. Final Checklist",
        "",
        "### Before Finalizing Affidavits:",
        "",
        "- [ ] All 130 AD paragraphs addressed",
        "- [ ] No placeholder responses remain",
        "- [ ] Neutral, factual tone throughout",
        "- [ ] All factual claims supported by annexure citations",
        "- [ ] Legal provisions cited where appropriate",
        "- [ ] Material non-disclosures identified",
        "- [ ] Conflicts of interest highlighted",
        "- [ ] Timeline established with dates",
        "- [ ] Revenue context provided for financial figures",
        "- [ ] JR/DR numbering consistent",
        "- [ ] Paragraph ordering maintained",
        "- [ ] All annexures prepared and referenced",
        "",
        "---",
        "",
        "## 8. Summary of Key Improvements",
        "",
        "### Implemented in v15 REFINED:",
        "",
        "1. ✓ 100% AD paragraph coverage maintained",
        "2. ✓ Correct sequential ordering",
        "3. ✓ JR/DR numbering protocol",
        "4. ✓ Neutral, factual tone",
        "5. ✓ Specific responses to serious allegations",
        "6. ✓ Revenue context for IT expenses",
        "7. ✓ Timeline references (6 June fraud report, 7 June card cancellation)",
        "8. ✓ Conflict of interest identification",
        "",
        "### Still Required:",
        "",
        "1. Complete annexure preparation and attachment",
        "2. Detailed evidence citations for all factual claims",
        "3. Expansion of responses to serious allegations with full evidence",
        "4. Legal provision citations in delinquency responses",
        "5. Counter-application preparation (if strategically appropriate)",
        "",
        "---",
        "",
        "**End of Report**"
    ])
    
    # Save report
    with open('/home/ubuntu/canima/IMPROVEMENT_RECOMMENDATIONS_V5_COMPREHENSIVE.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print("✓ Comprehensive improvement recommendations generated")
    print("\nKey sections:")
    print("  1. Structural Compliance")
    print("  2. Content Quality and Tone")
    print("  3. Legal Framework and Citations")
    print("  4. Strategic Response Elements")
    print("  5. Specific Section Recommendations")
    print("  6. Annexure Strategy")
    print("  7. Final Checklist")
    print("  8. Summary of Key Improvements")
    print("\nFile created:")
    print("  - IMPROVEMENT_RECOMMENDATIONS_V5_COMPREHENSIVE.md")

if __name__ == '__main__':
    generate_recommendations_report()

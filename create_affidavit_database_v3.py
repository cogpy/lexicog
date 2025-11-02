#!/usr/bin/env python3
"""
Create a comprehensive SQLite database for managing affidavit data.
Properly imports CSV files with correct column mapping.
"""
import sqlite3
import csv
from pathlib import Path
from datetime import datetime

# Configuration
DB_PATH = Path("/home/ubuntu/canima/database/affidavit_data.db")
CSV_DIR = Path("/home/ubuntu/upload")
CORRECT_AD_REF = Path("/home/ubuntu/upload/ad_sorted_correct.txt")

# CSV files to import
CSV_FILES = {
    "ad_paragraphs": "ad_paragraphs_20251102_185032.csv",
    "affidavit_sections": "affidavit_sections_20251102_185041.csv",
    "comments": "comments_20251102_185048.csv",
    "jr_responses": "jr_responses_20251102_185344.csv",
    "dr_responses": "dr_responses_20251102_185334.csv"
}

def create_database_schema(conn):
    """Create the database schema with all necessary tables."""
    cursor = conn.cursor()
    
    # Table 1: AD Paragraphs (Correct 141-paragraph reference)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ad_paragraphs_reference (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad_number TEXT UNIQUE NOT NULL,
            sequence_order INTEGER UNIQUE NOT NULL,
            section_number INTEGER,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Table 2: AD Paragraphs (from CSV)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ad_paragraphs_csv (
            id INTEGER PRIMARY KEY,
            section_id INTEGER,
            paragraph_number TEXT,
            content TEXT,
            created_at TEXT,
            updated_at TEXT,
            parent_id TEXT,
            order_index INTEGER,
            notes TEXT
        )
    ''')
    
    # Table 3: Affidavit Sections
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS affidavit_sections (
            id INTEGER PRIMARY KEY,
            title TEXT,
            description TEXT,
            order_index INTEGER,
            created_at TEXT,
            updated_at TEXT
        )
    ''')
    
    # Table 4: JR Responses (mapped from CSV: paragraph_number -> jr_number, content -> response_text)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jr_responses (
            id INTEGER PRIMARY KEY,
            section_id INTEGER,
            jr_number TEXT,
            response_text TEXT,
            created_at TEXT,
            updated_at TEXT,
            evidence_strength INTEGER,
            annexures TEXT
        )
    ''')
    
    # Table 5: DR Responses (mapped from CSV: paragraph_number -> dr_number, content -> response_text)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dr_responses (
            id INTEGER PRIMARY KEY,
            section_id INTEGER,
            dr_number TEXT,
            response_text TEXT,
            created_at TEXT,
            updated_at TEXT,
            evidence_strength INTEGER,
            annexures TEXT
        )
    ''')
    
    # Table 6: AD Number Reconciliation
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ad_reconciliation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad_number_correct TEXT NOT NULL,
            ad_number_csv TEXT,
            csv_id INTEGER,
            has_jr_response INTEGER DEFAULT 0,
            has_dr_response INTEGER DEFAULT 0,
            reconciliation_status TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    print("✓ Database schema created")

def import_correct_ad_reference(conn):
    """Import the correct 141-paragraph AD reference."""
    cursor = conn.cursor()
    
    with open(CORRECT_AD_REF, 'r') as f:
        ad_numbers = [line.strip().replace('AD ', '') for line in f if line.strip()]
    
    for idx, ad_num in enumerate(ad_numbers, 1):
        # Extract section number (first digit)
        section_num = int(ad_num.split('.')[0]) if '.' in ad_num else int(ad_num)
        
        cursor.execute('''
            INSERT OR IGNORE INTO ad_paragraphs_reference 
            (ad_number, sequence_order, section_number)
            VALUES (?, ?, ?)
        ''', (ad_num, idx, section_num))
    
    conn.commit()
    print(f"✓ Imported {len(ad_numbers)} AD paragraphs from correct reference")

def import_responses_csv(conn, table_name, csv_file, response_prefix):
    """Import JR or DR responses CSV with proper column mapping."""
    csv_path = CSV_DIR / csv_file
    if not csv_path.exists():
        print(f"⚠ CSV file not found: {csv_file}")
        return 0
    
    cursor = conn.cursor()
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
        if not rows:
            print(f"⚠ No data in CSV file: {csv_file}")
            return 0
        
        # Map CSV columns to database columns
        # CSV: id, section_id, paragraph_number, content, createdAt, updatedAt, evidence_strength, annexures
        # DB:  id, section_id, jr/dr_number, response_text, created_at, updated_at, evidence_strength, annexures
        
        inserted_count = 0
        for row in rows:
            try:
                cursor.execute(f'''
                    INSERT OR REPLACE INTO {table_name} 
                    (id, section_id, {response_prefix}_number, response_text, created_at, updated_at, evidence_strength, annexures)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    row.get('id'),
                    row.get('section_id'),
                    row.get('paragraph_number'),  # This is the AD paragraph number
                    row.get('content'),           # This is the response text
                    row.get('createdAt'),
                    row.get('updatedAt'),
                    row.get('evidence_strength'),
                    row.get('annexures')
                ))
                inserted_count += 1
            except Exception as e:
                print(f"⚠ Error inserting row {row.get('id')}: {e}")
                continue
        
        conn.commit()
        print(f"✓ Imported {inserted_count} rows into {table_name}")
        return inserted_count

def import_ad_paragraphs_csv(conn):
    """Import AD paragraphs CSV."""
    csv_path = CSV_DIR / CSV_FILES["ad_paragraphs"]
    if not csv_path.exists():
        print(f"⚠ CSV file not found: {CSV_FILES['ad_paragraphs']}")
        return 0
    
    cursor = conn.cursor()
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
        inserted_count = 0
        for row in rows:
            try:
                cursor.execute('''
                    INSERT OR REPLACE INTO ad_paragraphs_csv 
                    (id, section_id, paragraph_number, content, created_at, updated_at, parent_id, order_index, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    row.get('id'),
                    row.get('section_id'),
                    row.get('paragraph_number'),
                    row.get('content'),
                    row.get('createdAt'),
                    row.get('updatedAt'),
                    row.get('parent_id'),
                    row.get('order_index'),
                    row.get('notes')
                ))
                inserted_count += 1
            except Exception as e:
                print(f"⚠ Error inserting row: {e}")
                continue
        
        conn.commit()
        print(f"✓ Imported {inserted_count} rows into ad_paragraphs_csv")
        return inserted_count

def reconcile_ad_numbers(conn):
    """Reconcile AD numbers between correct reference and CSV data."""
    cursor = conn.cursor()
    
    # Get all correct AD numbers
    cursor.execute('SELECT ad_number, sequence_order FROM ad_paragraphs_reference ORDER BY sequence_order')
    correct_ads = cursor.fetchall()
    
    # Get all CSV AD numbers
    cursor.execute('SELECT id, paragraph_number FROM ad_paragraphs_csv')
    csv_ads = cursor.fetchall()
    csv_ad_dict = {row[1]: row[0] for row in csv_ads if row[1]}
    
    # Get JR responses
    cursor.execute('SELECT jr_number FROM jr_responses WHERE jr_number IS NOT NULL')
    jr_responses = set([row[0] for row in cursor.fetchall()])
    
    # Get DR responses
    cursor.execute('SELECT dr_number FROM dr_responses WHERE dr_number IS NOT NULL')
    dr_responses = set([row[0] for row in cursor.fetchall()])
    
    reconciliation_count = 0
    matched = 0
    missing = 0
    
    for ad_num, seq_order in correct_ads:
        # Check if this AD number exists in CSV
        if ad_num in csv_ad_dict:
            status = "MATCHED"
            csv_id = csv_ad_dict[ad_num]
            matched += 1
        else:
            status = "MISSING_IN_CSV"
            csv_id = None
            missing += 1
        
        # Check if we have responses
        has_jr = 1 if ad_num in jr_responses else 0
        has_dr = 1 if ad_num in dr_responses else 0
        
        cursor.execute('''
            INSERT INTO ad_reconciliation 
            (ad_number_correct, ad_number_csv, csv_id, has_jr_response, has_dr_response, reconciliation_status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (ad_num, ad_num if csv_id else None, csv_id, has_jr, has_dr, status))
        
        reconciliation_count += 1
    
    # Check for CSV AD numbers that don't match correct reference
    extra = 0
    for csv_ad, csv_id in csv_ad_dict.items():
        if csv_ad not in [ad[0] for ad in correct_ads]:
            cursor.execute('''
                INSERT INTO ad_reconciliation 
                (ad_number_correct, ad_number_csv, csv_id, reconciliation_status, notes)
                VALUES (?, ?, ?, ?, ?)
            ''', (None, csv_ad, csv_id, "EXTRA_IN_CSV", "AD number in CSV but not in correct reference"))
            extra += 1
    
    conn.commit()
    print(f"✓ Reconciled {reconciliation_count} AD paragraphs")
    print(f"  - Matched: {matched}")
    print(f"  - Missing in CSV: {missing}")
    print(f"  - Extra in CSV: {extra}")
    print(f"  - JR responses: {len(jr_responses)}")
    print(f"  - DR responses: {len(dr_responses)}")

def generate_reconciliation_report(conn):
    """Generate a reconciliation report."""
    cursor = conn.cursor()
    
    # Count reconciliation statuses
    cursor.execute('''
        SELECT reconciliation_status, COUNT(*) 
        FROM ad_reconciliation 
        GROUP BY reconciliation_status
    ''')
    status_counts = cursor.fetchall()
    
    report = "# AD Paragraph Reconciliation Report\n\n"
    report += f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += f"**Database:** {DB_PATH}\n\n"
    report += "## Summary\n\n"
    
    total = sum([count for _, count in status_counts])
    for status, count in status_counts:
        percentage = (count / total * 100) if total > 0 else 0
        report += f"- **{status}:** {count} ({percentage:.1f}%)\n"
    
    # Response coverage
    cursor.execute('SELECT COUNT(*) FROM ad_reconciliation WHERE has_jr_response = 1')
    jr_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM ad_reconciliation WHERE has_dr_response = 1')
    dr_count = cursor.fetchone()[0]
    
    report += f"\n## Response Coverage\n\n"
    report += f"- **JR Responses:** {jr_count} / 141 ({jr_count/141*100:.1f}%)\n"
    report += f"- **DR Responses:** {dr_count} / 141 ({dr_count/141*100:.1f}%)\n"
    
    # Get missing paragraphs
    cursor.execute('''
        SELECT ad_number_correct, has_jr_response, has_dr_response
        FROM ad_reconciliation 
        WHERE reconciliation_status = 'MISSING_IN_CSV'
        ORDER BY ad_number_correct
    ''')
    missing = cursor.fetchall()
    
    if missing:
        report += f"\n## Missing AD Paragraphs ({len(missing)})\n\n"
        report += "These AD paragraphs exist in the correct 141-paragraph reference but are missing from the CSV data:\n\n"
        for ad_num, has_jr, has_dr in missing:
            jr_status = "✓" if has_jr else "✗"
            dr_status = "✓" if has_dr else "✗"
            report += f"- AD {ad_num} (JR: {jr_status}, DR: {dr_status})\n"
    
    # Database statistics
    cursor.execute('SELECT COUNT(*) FROM ad_paragraphs_reference')
    ref_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM ad_paragraphs_csv')
    csv_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM jr_responses')
    jr_total = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM dr_responses')
    dr_total = cursor.fetchone()[0]
    
    report += f"\n## Database Statistics\n\n"
    report += f"- **AD Paragraphs (Reference):** {ref_count}\n"
    report += f"- **AD Paragraphs (CSV):** {csv_count}\n"
    report += f"- **JR Responses (Total):** {jr_total}\n"
    report += f"- **DR Responses (Total):** {dr_total}\n"
    
    return report

def main():
    print("Creating affidavit database...")
    print(f"Target: {DB_PATH}\n")
    
    # Ensure database directory exists
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    # Remove existing database
    if DB_PATH.exists():
        DB_PATH.unlink()
        print("✓ Removed existing database\n")
    
    # Create database connection
    conn = sqlite3.connect(DB_PATH)
    
    try:
        # Create schema
        create_database_schema(conn)
        
        # Import correct AD reference
        import_correct_ad_reference(conn)
        
        # Import CSV files
        print("\nImporting CSV files...")
        import_ad_paragraphs_csv(conn)
        import_responses_csv(conn, "jr_responses", CSV_FILES["jr_responses"], "jr")
        import_responses_csv(conn, "dr_responses", CSV_FILES["dr_responses"], "dr")
        
        # Reconcile AD numbers
        print("\nReconciling AD numbers...")
        reconcile_ad_numbers(conn)
        
        # Generate report
        print("\nGenerating reconciliation report...")
        report = generate_reconciliation_report(conn)
        
        # Save report
        report_path = DB_PATH.parent / "AD_RECONCILIATION_REPORT.md"
        report_path.write_text(report)
        print(f"✓ Saved reconciliation report to {report_path}")
        
        print(f"\n✓ Database created successfully at {DB_PATH}")
        print(f"✓ Total size: {DB_PATH.stat().st_size / 1024:.2f} KB")
        
    finally:
        conn.close()

if __name__ == "__main__":
    main()


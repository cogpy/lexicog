#!/usr/bin/env python3
"""
Create a comprehensive SQLite database for managing affidavit data.
Imports all CSV files and reconciles AD paragraph numbers with the correct 141-paragraph reference.
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
    "dr_responses_old": "dr_responses_20251102_185059.csv",
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
    
    # Table 2: AD Paragraphs (from CSV - may have incorrect numbering)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ad_paragraphs_csv (
            id INTEGER PRIMARY KEY,
            section_id INTEGER,
            ad_number_original TEXT,
            content TEXT,
            created_at TEXT,
            updated_at TEXT,
            parent_id INTEGER,
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
    
    # Table 4: Comments
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY,
            ad_paragraph_id INTEGER,
            comment_text TEXT,
            comment_type TEXT,
            created_at TEXT,
            updated_at TEXT,
            author TEXT
        )
    ''')
    
    # Table 5: JR Responses
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jr_responses (
            id INTEGER PRIMARY KEY,
            ad_paragraph_id INTEGER,
            jr_number TEXT,
            response_text TEXT,
            response_type TEXT,
            created_at TEXT,
            updated_at TEXT,
            status TEXT
        )
    ''')
    
    # Table 6: DR Responses
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dr_responses (
            id INTEGER PRIMARY KEY,
            ad_paragraph_id INTEGER,
            dr_number TEXT,
            response_text TEXT,
            response_type TEXT,
            created_at TEXT,
            updated_at TEXT,
            status TEXT
        )
    ''')
    
    # Table 7: AD Number Reconciliation
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ad_reconciliation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad_number_correct TEXT NOT NULL,
            ad_number_csv TEXT,
            csv_id INTEGER,
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

def import_csv_file(conn, table_name, csv_file):
    """Import a CSV file into the specified table."""
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
        
        # Get column names from CSV
        columns = list(rows[0].keys())
        
        # Create placeholders for SQL INSERT
        placeholders = ','.join(['?' for _ in columns])
        column_names = ','.join(columns)
        
        # Insert data
        for row in rows:
            values = [row[col] for col in columns]
            cursor.execute(f'''
                INSERT OR REPLACE INTO {table_name} ({column_names})
                VALUES ({placeholders})
            ''', values)
        
        conn.commit()
        print(f"✓ Imported {len(rows)} rows into {table_name}")
        return len(rows)

def reconcile_ad_numbers(conn):
    """Reconcile AD numbers between correct reference and CSV data."""
    cursor = conn.cursor()
    
    # Get all correct AD numbers
    cursor.execute('SELECT ad_number, sequence_order FROM ad_paragraphs_reference ORDER BY sequence_order')
    correct_ads = cursor.fetchall()
    
    # Get all CSV AD numbers
    cursor.execute('SELECT id, ad_number_original FROM ad_paragraphs_csv')
    csv_ads = cursor.fetchall()
    
    # Create a mapping
    csv_ad_dict = {row[1]: row[0] for row in csv_ads if row[1]}
    
    reconciliation_count = 0
    for ad_num, seq_order in correct_ads:
        # Check if this AD number exists in CSV
        if ad_num in csv_ad_dict:
            status = "MATCHED"
            csv_id = csv_ad_dict[ad_num]
        else:
            status = "MISSING_IN_CSV"
            csv_id = None
        
        cursor.execute('''
            INSERT INTO ad_reconciliation 
            (ad_number_correct, ad_number_csv, csv_id, reconciliation_status)
            VALUES (?, ?, ?, ?)
        ''', (ad_num, ad_num if csv_id else None, csv_id, status))
        
        reconciliation_count += 1
    
    # Check for CSV AD numbers that don't match correct reference
    for csv_ad, csv_id in csv_ad_dict.items():
        if csv_ad not in [ad[0] for ad in correct_ads]:
            cursor.execute('''
                INSERT INTO ad_reconciliation 
                (ad_number_correct, ad_number_csv, csv_id, reconciliation_status, notes)
                VALUES (?, ?, ?, ?, ?)
            ''', (None, csv_ad, csv_id, "EXTRA_IN_CSV", "AD number in CSV but not in correct reference"))
    
    conn.commit()
    print(f"✓ Reconciled {reconciliation_count} AD paragraphs")

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
    report += f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    report += "## Summary\n\n"
    
    for status, count in status_counts:
        report += f"- **{status}:** {count}\n"
    
    # Get missing paragraphs
    cursor.execute('''
        SELECT ad_number_correct 
        FROM ad_reconciliation 
        WHERE reconciliation_status = 'MISSING_IN_CSV'
        ORDER BY ad_number_correct
    ''')
    missing = cursor.fetchall()
    
    if missing:
        report += f"\n## Missing AD Paragraphs ({len(missing)})\n\n"
        for ad_num, in missing:
            report += f"- AD {ad_num}\n"
    
    # Get extra paragraphs
    cursor.execute('''
        SELECT ad_number_csv 
        FROM ad_reconciliation 
        WHERE reconciliation_status = 'EXTRA_IN_CSV'
        ORDER BY ad_number_csv
    ''')
    extra = cursor.fetchall()
    
    if extra:
        report += f"\n## Extra AD Paragraphs in CSV ({len(extra)})\n\n"
        for ad_num, in extra:
            report += f"- AD {ad_num}\n"
    
    return report

def main():
    print("Creating affidavit database...")
    
    # Ensure database directory exists
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    # Create database connection
    conn = sqlite3.connect(DB_PATH)
    
    try:
        # Create schema
        create_database_schema(conn)
        
        # Import correct AD reference
        import_correct_ad_reference(conn)
        
        # Import CSV files
        import_csv_file(conn, "ad_paragraphs_csv", CSV_FILES["ad_paragraphs"])
        import_csv_file(conn, "affidavit_sections", CSV_FILES["affidavit_sections"])
        import_csv_file(conn, "comments", CSV_FILES["comments"])
        import_csv_file(conn, "jr_responses", CSV_FILES["jr_responses"])
        import_csv_file(conn, "dr_responses", CSV_FILES["dr_responses"])
        
        # Reconcile AD numbers
        reconcile_ad_numbers(conn)
        
        # Generate report
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


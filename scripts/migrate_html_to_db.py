#!/usr/bin/env python3
"""
Migration script: Extract verses from index.html and populate SQLite database.

This script parses the HTML file containing Pāśupatasūtra and Vivekamārtaṇḍa verses
and inserts them into the database with all fields preserved.
"""

import re
import sqlite3
import shutil
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
HTML_FILE = PROJECT_ROOT / 'index.html'
DATABASE_FILE = PROJECT_ROOT / 'database' / 'vivekamartanda.db'
SCHEMA_FILE = PROJECT_ROOT / 'database' / 'schema.sql'
BACKUP_DIR = PROJECT_ROOT / 'backups'

# Text IDs (must match database)
TEXT_IDS = {
    'pasupatasutra': 1,
    'vivekamartanda': 2
}


def create_backup():
    """Create backup of HTML file before migration."""
    BACKUP_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = BACKUP_DIR / f'index_{timestamp}.html'
    shutil.copy(HTML_FILE, backup_path)
    print(f"✓ Created backup: {backup_path}")
    return backup_path


def init_database():
    """Initialize database with schema."""
    DATABASE_FILE.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DATABASE_FILE)
    with open(SCHEMA_FILE, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("✓ Database initialized")


def clean_html(text):
    """Clean HTML tags from text content."""
    if not text:
        return ""
    # Remove HTML tags but keep content
    text = re.sub(r'<br\s*/?>', '\n', text)
    soup = BeautifulSoup(text, 'html.parser')
    return soup.get_text().strip()


def extract_cell_html(cell):
    """Extract HTML content from table cell, preserving formatting."""
    if not cell:
        return ""
    # Get inner HTML
    return ''.join(str(content) for content in cell.contents).strip()


def parse_verses_from_html():
    """Parse all verses from the HTML file."""
    print(f"\nParsing {HTML_FILE}...")

    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    verses_data = []
    current_text_id = TEXT_IDS['vivekamartanda']  # Default
    current_section = None
    display_order = 0

    # Find all HTML comments that mark verses
    from bs4 import Comment

    for element in soup.descendants:
        # Check if it's an HTML comment
        if isinstance(element, Comment):
            comment_text = str(element).strip()

            # Check if it's a verse comment
            verse_match = re.search(r'Verse\s+(\d+|inv-\d+)', comment_text, re.IGNORECASE)
            if not verse_match:
                continue

            verse_number = verse_match.group(1)

            # Find the next <tr> element after this comment
            next_element = element.next_element
            while next_element:
                if next_element.name == 'tr':
                    row = next_element
                    break
                next_element = next_element.next_sibling
            else:
                print(f"⚠️  No <tr> found after verse comment: {verse_number}")
                continue

            # Get all cells
            cells = row.select('td')
            if len(cells) < 5:
                # Check if this is a section header
                section_cell = row.select_one('td.section-header')
                if section_cell:
                    current_section = section_cell.get_text().strip()
                continue

            # Extract data from cells
            verse_data = {
                'text_id': current_text_id,
                'verse_number': verse_number,
                'section_header': current_section,
                'display_order': display_order,
            }

            # Column order: Sanskrit | Word Analysis | Literal Translation | Grammar | Jim's
            # Sanskrit text (may have de-sandhi)
            sanskrit_cell = cells[0]
            sanskrit_full = extract_cell_html(sanskrit_cell)

            # Check if there's de-sandhi
            desandhi_match = re.search(r'<em>De-sandhi:</em><br\s*/?>(.*?)$', sanskrit_full, re.DOTALL | re.IGNORECASE)
            if desandhi_match:
                verse_data['sanskrit_desandhi'] = clean_html(desandhi_match.group(1))
                # Remove de-sandhi from main text
                verse_data['sanskrit_text'] = re.sub(r'<br\s*/?>\s*<em>De-sandhi:.*', '', sanskrit_full, flags=re.DOTALL | re.IGNORECASE).strip()
            else:
                verse_data['sanskrit_text'] = sanskrit_full
                verse_data['sanskrit_desandhi'] = None

            # Word analysis (editable) - has contenteditable="true"
            verse_data['word_analysis'] = extract_cell_html(cells[1]) if len(cells) > 1 else None

            # Literal translation (editable) - may be class="translation"
            verse_data['literal_translation'] = extract_cell_html(cells[2]) if len(cells) > 2 else None

            # Grammar summary
            verse_data['grammar_summary'] = extract_cell_html(cells[3]) if len(cells) > 3 else None

            # Jim's translation
            verse_data['jims_translation'] = extract_cell_html(cells[4]) if len(cells) > 4 else None

            verses_data.append(verse_data)
            display_order += 1

            print(f"  ✓ Verse {verse_number}")

    print(f"\n✓ Extracted {len(verses_data)} verses")
    return verses_data


def insert_verses(verses_data):
    """Insert parsed verses into database."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    inserted = 0
    for verse in verses_data:
        try:
            cursor.execute('''
                INSERT INTO verses (
                    text_id, verse_number, section_header,
                    sanskrit_text, sanskrit_desandhi,
                    word_analysis, literal_translation,
                    grammar_summary, jims_translation,
                    display_order
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                verse['text_id'],
                verse['verse_number'],
                verse.get('section_header'),
                verse['sanskrit_text'],
                verse.get('sanskrit_desandhi'),
                verse.get('word_analysis'),
                verse.get('literal_translation'),
                verse.get('grammar_summary'),
                verse.get('jims_translation'),
                verse['display_order']
            ))
            inserted += 1
        except sqlite3.IntegrityError as e:
            print(f"⚠️  Skipping duplicate verse {verse['verse_number']}: {e}")
        except Exception as e:
            print(f"❌ Error inserting verse {verse['verse_number']}: {e}")

    conn.commit()
    conn.close()
    print(f"✓ Inserted {inserted} verses into database")


def verify_migration():
    """Verify migration was successful."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # Count verses
    result = cursor.execute('SELECT COUNT(*) FROM verses').fetchone()
    total_verses = result[0]

    # Get verses per text
    texts = cursor.execute('''
        SELECT t.display_name, COUNT(v.verse_id) as count
        FROM texts t
        LEFT JOIN verses v ON t.text_id = v.text_id
        GROUP BY t.text_id
    ''').fetchall()

    conn.close()

    print("\n" + "=" * 60)
    print("MIGRATION VERIFICATION")
    print("=" * 60)
    print(f"Total verses: {total_verses}")
    for text_name, count in texts:
        print(f"  {text_name}: {count} verses")
    print("=" * 60)


def main():
    print("=" * 60)
    print("HTML → SQLite Migration Script")
    print("=" * 60)

    # Step 1: Backup
    print("\n[1/5] Creating backup...")
    create_backup()

    # Step 2: Initialize database
    print("\n[2/5] Initializing database...")
    init_database()

    # Step 3: Parse HTML
    print("\n[3/5] Parsing verses from HTML...")
    verses_data = parse_verses_from_html()

    if not verses_data:
        print("❌ No verses found in HTML file!")
        return 1

    # Step 4: Insert into database
    print("\n[4/5] Inserting verses into database...")
    insert_verses(verses_data)

    # Step 5: Verify
    print("\n[5/5] Verifying migration...")
    verify_migration()

    print("\n✅ Migration complete!")
    print(f"\nDatabase: {DATABASE_FILE}")
    print("Next step: Start the Flask API server")
    print("  python3 backend/app.py")

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())

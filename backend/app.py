#!/usr/bin/env python3
"""
Flask API backend for Sanskrit text translation tool.
Provides REST API for editable verse translations with auto-save functionality.
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS

# Configuration
DATABASE_PATH = Path(__file__).parent.parent / 'database' / 'vivekamartanda.db'
SCHEMA_PATH = Path(__file__).parent.parent / 'database' / 'schema.sql'

app = Flask(__name__)
CORS(app)  # Enable CORS for local development

# ============================================================================
# Database Helper Functions
# ============================================================================

def get_db_connection():
    """Create database connection with row factory for dict-like access."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """Initialize database with schema if it doesn't exist."""
    if not DATABASE_PATH.exists():
        print(f"Creating database at {DATABASE_PATH}")
        DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(DATABASE_PATH)
        with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()
        print("✓ Database initialized")


# ============================================================================
# API Endpoints
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'database': str(DATABASE_PATH),
        'exists': DATABASE_PATH.exists()
    })


@app.route('/api/texts', methods=['GET'])
def get_texts():
    """Get list of all texts."""
    conn = get_db_connection()
    texts = conn.execute('SELECT * FROM texts ORDER BY text_id').fetchall()
    conn.close()

    return jsonify({
        'success': True,
        'texts': [dict(row) for row in texts]
    })


@app.route('/api/texts/<int:text_id>', methods=['GET'])
def get_text(text_id):
    """Get specific text metadata."""
    conn = get_db_connection()
    text = conn.execute('SELECT * FROM texts WHERE text_id = ?', (text_id,)).fetchone()
    conn.close()

    if text is None:
        return jsonify({'success': False, 'error': 'Text not found'}), 404

    return jsonify({
        'success': True,
        'text': dict(text)
    })


@app.route('/api/verses/<int:text_id>', methods=['GET'])
def get_verses_by_text(text_id):
    """Get all verses for a specific text."""
    conn = get_db_connection()
    verses = conn.execute('''
        SELECT * FROM verses
        WHERE text_id = ?
        ORDER BY display_order
    ''', (text_id,)).fetchall()
    conn.close()

    return jsonify({
        'success': True,
        'text_id': text_id,
        'count': len(verses),
        'verses': [dict(row) for row in verses]
    })


@app.route('/api/verses/<int:text_id>/<verse_number>', methods=['GET'])
def get_verse(text_id, verse_number):
    """Get specific verse by text_id and verse_number."""
    conn = get_db_connection()
    verse = conn.execute('''
        SELECT * FROM verses
        WHERE text_id = ? AND verse_number = ?
    ''', (text_id, verse_number)).fetchone()
    conn.close()

    if verse is None:
        return jsonify({'success': False, 'error': 'Verse not found'}), 404

    return jsonify({
        'success': True,
        'verse': dict(verse)
    })


@app.route('/api/verses/<int:verse_id>', methods=['PUT'])
def update_verse(verse_id):
    """Update verse fields (for auto-save)."""
    data = request.get_json()

    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400

    # Allowed editable fields
    editable_fields = ['word_analysis', 'literal_translation']

    # Build UPDATE query dynamically
    updates = []
    values = []

    for field in editable_fields:
        if field in data:
            updates.append(f'{field} = ?')
            values.append(data[field])

    if not updates:
        return jsonify({'success': False, 'error': 'No editable fields provided'}), 400

    # Add verse_id to values
    values.append(verse_id)

    # Execute update
    conn = get_db_connection()
    cursor = conn.cursor()

    query = f"UPDATE verses SET {', '.join(updates)} WHERE verse_id = ?"

    try:
        cursor.execute(query, values)
        conn.commit()

        # Get updated verse
        verse = conn.execute('SELECT * FROM verses WHERE verse_id = ?', (verse_id,)).fetchone()
        conn.close()

        return jsonify({
            'success': True,
            'verse_id': verse_id,
            'updated_fields': list(data.keys()),
            'verse': dict(verse)
        })

    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/verses/<int:verse_id>/field/<field_name>', methods=['PATCH'])
def update_verse_field(verse_id, field_name):
    """Update a single field of a verse (alternative endpoint)."""
    data = request.get_json()

    if 'value' not in data:
        return jsonify({'success': False, 'error': 'No value provided'}), 400

    # Security: only allow editable fields
    editable_fields = ['word_analysis', 'literal_translation']
    if field_name not in editable_fields:
        return jsonify({'success': False, 'error': 'Field not editable'}), 403

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            f"UPDATE verses SET {field_name} = ? WHERE verse_id = ?",
            (data['value'], verse_id)
        )
        conn.commit()

        # Get updated verse
        verse = conn.execute('SELECT * FROM verses WHERE verse_id = ?', (verse_id,)).fetchone()
        conn.close()

        return jsonify({
            'success': True,
            'verse_id': verse_id,
            'field': field_name,
            'verse': dict(verse)
        })

    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/search', methods=['GET'])
def search_verses():
    """Search verses by keyword."""
    query = request.args.get('q', '')
    text_id = request.args.get('text_id', type=int)

    if not query:
        return jsonify({'success': False, 'error': 'No search query provided'}), 400

    conn = get_db_connection()

    sql = '''
        SELECT * FROM verses
        WHERE (
            sanskrit_text LIKE ? OR
            word_analysis LIKE ? OR
            literal_translation LIKE ? OR
            grammar_summary LIKE ?
        )
    '''
    params = [f'%{query}%'] * 4

    if text_id:
        sql += ' AND text_id = ?'
        params.append(text_id)

    sql += ' ORDER BY text_id, display_order'

    verses = conn.execute(sql, params).fetchall()
    conn.close()

    return jsonify({
        'success': True,
        'query': query,
        'count': len(verses),
        'verses': [dict(row) for row in verses]
    })


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get database statistics."""
    conn = get_db_connection()

    stats = {
        'texts': {},
        'total_verses': 0,
        'last_updated': None
    }

    # Get verse counts per text
    texts = conn.execute('SELECT * FROM texts').fetchall()
    for text in texts:
        count = conn.execute('SELECT COUNT(*) as cnt FROM verses WHERE text_id = ?',
                            (text['text_id'],)).fetchone()['cnt']
        stats['texts'][text['name']] = {
            'display_name': text['display_name'],
            'verse_count': count
        }
        stats['total_verses'] += count

    # Get last update timestamp
    last = conn.execute('SELECT MAX(updated_at) as last FROM verses').fetchone()
    if last and last['last']:
        stats['last_updated'] = last['last']

    conn.close()

    return jsonify({
        'success': True,
        'stats': stats
    })


# ============================================================================
# Error Handlers
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500


# ============================================================================
# Main
# ============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("Sanskrit Translation Tool - API Server")
    print("=" * 60)

    # Initialize database
    init_database()

    # Check if database has data
    conn = get_db_connection()
    verse_count = conn.execute('SELECT COUNT(*) as cnt FROM verses').fetchone()['cnt']
    conn.close()

    if verse_count == 0:
        print("\n⚠️  WARNING: Database is empty!")
        print("Run the migration script first:")
        print("  python3 scripts/migrate_html_to_db.py")
        print()
    else:
        print(f"\n✓ Database loaded with {verse_count} verses")

    print("\nAPI Endpoints:")
    print("  GET  /api/health")
    print("  GET  /api/texts")
    print("  GET  /api/verses/<text_id>")
    print("  PUT  /api/verses/<verse_id>")
    print("  GET  /api/search?q=keyword")
    print("  GET  /api/stats")
    print("\nStarting server on http://localhost:5000")
    print("=" * 60)
    print()

    app.run(debug=True, host='0.0.0.0', port=5000)

# Database Migration Plan - Vivekamārtaṇḍa Translation Tool

## Overview
Migrate from JSONbin cloud storage to proper database backend with auto-save functionality for editable translation and vocabulary columns.

## Goals
1. ✅ Keep existing UX (contenteditable cells, auto-save after 2s)
2. ✅ Store all verse data in database
3. ✅ Enable real-time editing and saving
4. ✅ Test locally before production deployment
5. ✅ Preserve all existing data
6. ✅ Support multiple texts (Pāśupatasūtra, Vivekamārtaṇḍa)

## Architecture

### Stack Choice: SQLite + Flask + Vanilla JS
- **SQLite**: Portable, serverless, perfect for local development
- **Flask**: Lightweight Python web framework, easy CORS setup
- **Frontend**: Keep existing HTML/JS, update API calls

### Database Schema

```sql
CREATE TABLE texts (
    text_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    display_name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE verses (
    verse_id INTEGER PRIMARY KEY AUTOINCREMENT,
    text_id INTEGER NOT NULL,
    verse_number TEXT NOT NULL,
    section_header TEXT,
    sanskrit_text TEXT NOT NULL,
    sanskrit_desandhi TEXT,
    word_analysis TEXT,
    literal_translation TEXT,
    grammar_summary TEXT,
    jims_translation TEXT,
    display_order INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (text_id) REFERENCES texts(text_id),
    UNIQUE(text_id, verse_number)
);

CREATE INDEX idx_verses_text ON verses(text_id);
CREATE INDEX idx_verses_order ON verses(text_id, display_order);
```

### API Endpoints

**Base URL**: `http://localhost:5000/api`

#### Texts
- `GET /texts` - List all texts
- `GET /texts/:id` - Get text metadata

#### Verses
- `GET /verses/:text_id` - Get all verses for a text
- `GET /verses/:text_id/:verse_number` - Get specific verse
- `PUT /verses/:verse_id` - Update verse (auto-save endpoint)
- `PATCH /verses/:verse_id/field` - Update single field

#### Example Request/Response

```javascript
// Update word analysis
PUT /api/verses/42
{
  "word_analysis": "prāṇaḥ = prāṇa (nom.)<br>...",
  "updated_at": "2025-11-05T10:30:00Z"
}

// Response
{
  "success": true,
  "verse_id": 42,
  "updated_fields": ["word_analysis", "updated_at"]
}
```

## Implementation Steps

### Phase 1: Local Setup (DO THIS FIRST)
1. ✅ Create SQLite database schema
2. ✅ Build Flask API with CORS enabled
3. ✅ Create migration script: HTML → SQLite
4. ✅ Test API endpoints with curl/Postman

### Phase 2: Frontend Update
1. ✅ Create `index-local.html` (copy of index.html)
2. ✅ Update JavaScript to use Flask API instead of JSONbin
3. ✅ Keep auto-save functionality (2s delay)
4. ✅ Add better error handling and save indicators

### Phase 3: Testing
1. ✅ Run Flask locally on port 5000
2. ✅ Open `index-local.html` in browser
3. ✅ Test editing and auto-save for both columns
4. ✅ Verify data persistence across page reloads
5. ✅ Test with both Pāśupatasūtra and Vivekamārtaṇḍa tabs

### Phase 4: Production Deployment (LATER)
- Options:
  - Railway.app (free tier, easy deployment)
  - Heroku (PostgreSQL addon)
  - DigitalOcean App Platform
  - Keep as localhost-only tool

## File Structure

```
pasupata-sutra-analysis/
├── index.html                    # Production (unchanged)
├── index-local.html              # Local dev with DB backend
├── database/
│   ├── schema.sql               # Database schema
│   ├── vivekamartanda.db        # SQLite database
│   └── migrations/
│       └── 001_initial.sql
├── backend/
│   ├── app.py                   # Flask application
│   ├── models.py                # Database models
│   ├── api.py                   # API routes
│   └── requirements.txt         # Python dependencies
├── scripts/
│   ├── migrate_html_to_db.py   # HTML → SQLite migration
│   ├── start_local_dev.sh       # Start Flask + open browser
│   └── backup_database.py       # Backup utility
└── DATABASE_MIGRATION_PLAN.md   # This file
```

## Migration Script Logic

```python
# Pseudocode for migrate_html_to_db.py

1. Parse index.html
2. Extract all verses from both texts
3. For each verse:
   - Extract verse number from comment
   - Extract Sanskrit text (with de-sandhi)
   - Extract word analysis (editable column)
   - Extract literal translation (editable column)
   - Extract grammar summary
   - Extract Jim's translation
4. Insert into database with proper text_id
5. Maintain display_order based on HTML order
6. Create backup of original HTML
7. Verify all data migrated correctly
```

## Frontend JavaScript Changes

```javascript
// OLD: JSONbin API
const JSONBIN_API_KEY = '...';
const JSONBIN_BIN_ID = '...';

fetch(`https://api.jsonbin.io/v3/b/${binId}`, {
  headers: { 'X-Master-Key': apiKey }
});

// NEW: Local Flask API
const API_BASE = 'http://localhost:5000/api';

fetch(`${API_BASE}/verses/${textId}/${verseNumber}`, {
  method: 'PUT',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ word_analysis: newValue })
});
```

## Benefits

1. **Proper Data Model**: Structured schema vs JSON blobs
2. **Better Querying**: SQL queries for filtering, searching
3. **Version Control**: Track changes with updated_at timestamps
4. **No API Limits**: No JSONbin rate limits
5. **Offline Work**: Works without internet (localhost)
6. **Future Features**: Easy to add search, export, diff views

## Risks & Mitigation

| Risk | Mitigation |
|------|------------|
| Breaking production | Keep index.html unchanged, test in index-local.html |
| Data loss during migration | Create backup before running migration |
| CORS issues | Enable CORS in Flask with flask-cors |
| Database corruption | Regular backups, use WAL mode for SQLite |

## Testing Checklist

- [ ] Database schema creates successfully
- [ ] Migration script extracts all verses correctly
- [ ] Flask API responds to all endpoints
- [ ] Frontend connects to local API
- [ ] Auto-save works (2s delay)
- [ ] Both editable columns save properly
- [ ] Page reload preserves changes
- [ ] Both text tabs work (Pāśupatasūtra, Vivekamārtaṇḍa)
- [ ] No console errors in browser
- [ ] Database file is portable

## Next Steps

1. **START**: Create database schema (`database/schema.sql`)
2. Build Flask API (`backend/app.py`)
3. Create migration script (`scripts/migrate_html_to_db.py`)
4. Test migration on copy of data
5. Create local HTML variant (`index-local.html`)
6. Update frontend JavaScript
7. Test full workflow
8. Document deployment options

## Timeline

- **Phase 1-2**: ~2-3 hours (database + API)
- **Phase 3**: ~1 hour (frontend updates)
- **Phase 4**: ~1 hour (testing)
- **Total**: ~4-5 hours for complete local system

## Future Enhancements

- Full-text search across verses
- Change history / undo functionality
- Export to various formats (PDF, DOCX, LaTeX)
- Collaborative editing (multi-user)
- Mobile-responsive interface
- Integration with Sanskrit dictionaries

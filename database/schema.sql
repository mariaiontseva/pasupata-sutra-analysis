-- Database schema for Sanskrit text translation tool
-- SQLite database for Vivekamārtaṇḍa and Pāśupatasūtra verses

-- Enable foreign keys
PRAGMA foreign_keys = ON;

-- Enable WAL mode for better concurrent access
PRAGMA journal_mode = WAL;

-- Texts table: stores metadata about each Sanskrit text
CREATE TABLE IF NOT EXISTS texts (
    text_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,           -- e.g., 'vivekamartanda', 'pasupatasutra'
    display_name TEXT NOT NULL,          -- e.g., 'Vivekamārtaṇḍa'
    description TEXT,
    author TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Verses table: stores all verse data
CREATE TABLE IF NOT EXISTS verses (
    verse_id INTEGER PRIMARY KEY AUTOINCREMENT,
    text_id INTEGER NOT NULL,
    verse_number TEXT NOT NULL,          -- e.g., '1', '38', 'inv-1'
    section_header TEXT,                 -- Section headers like "SECTION 1: INVOCATORY VERSES"

    -- Sanskrit columns (read-only)
    sanskrit_text TEXT NOT NULL,         -- Main Sanskrit text
    sanskrit_desandhi TEXT,              -- De-sandhi version

    -- Editable columns
    word_analysis TEXT,                  -- Blue column - word-by-word analysis
    literal_translation TEXT,            -- Yellow column - literal translation

    -- Read-only reference columns
    grammar_summary TEXT,                -- Grammar notes/verse summary with roots
    jims_translation TEXT,               -- Jim Mallinson's translation (reference)

    -- Metadata
    display_order INTEGER NOT NULL,      -- Order in which verses appear
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (text_id) REFERENCES texts(text_id) ON DELETE CASCADE,
    UNIQUE(text_id, verse_number)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_verses_text ON verses(text_id);
CREATE INDEX IF NOT EXISTS idx_verses_order ON verses(text_id, display_order);
CREATE INDEX IF NOT EXISTS idx_verses_updated ON verses(updated_at DESC);

-- Insert initial text records
INSERT OR IGNORE INTO texts (name, display_name, description, author) VALUES
('pasupatasutra', 'Pāśupatasūtra', 'Ancient text on the Pāśupata system with commentary', 'Kauṇḍinya'),
('vivekamartanda', 'Vivekamārtaṇḍa', 'Classical Hatha yoga text on chakras, nadis, and practices', 'Gorakṣanātha');

-- Trigger to automatically update updated_at timestamp
CREATE TRIGGER IF NOT EXISTS update_verse_timestamp
AFTER UPDATE ON verses
FOR EACH ROW
BEGIN
    UPDATE verses SET updated_at = CURRENT_TIMESTAMP WHERE verse_id = NEW.verse_id;
END;

-- Create a view for easy querying with text names
CREATE VIEW IF NOT EXISTS verses_full AS
SELECT
    v.verse_id,
    v.verse_number,
    t.name AS text_name,
    t.display_name AS text_display_name,
    v.section_header,
    v.sanskrit_text,
    v.sanskrit_desandhi,
    v.word_analysis,
    v.literal_translation,
    v.grammar_summary,
    v.jims_translation,
    v.display_order,
    v.created_at,
    v.updated_at
FROM verses v
JOIN texts t ON v.text_id = t.text_id
ORDER BY v.text_id, v.display_order;

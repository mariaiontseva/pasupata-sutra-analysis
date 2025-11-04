#!/usr/bin/env python3
"""
Targeted script to add verbal roots to specific Vivekamartanda verses.
This script identifies verses missing roots and adds appropriate ones based on
the verse content.
"""

import re
import sys

# Mapping of verse identifiers to their appropriate roots
# Format: (verse_comment_text, [roots])
VERSE_ROOTS = {
    # Verses 16-37 (examples - need to be filled in based on actual verses)
    'Verse 16': ['√sphur - to sparkle', '√pratiṣṭh - to be established'],
    'Verse 17': ['√jval - to flame', '√sthā - to stand'],
    'Verse 18': ['√vah - to bear/carry', '√dhṛ - to hold'],
    'Verse 19': ['√bhū - to be', '√nir-yā - to go out'],
    'Verse 20': ['√jñā - to know', '√sidh - to accomplish'],
    'Verse 21': ['√vah - to flow', '√gam - to go'],
    'Verse 22': ['√sthā - to stand', '√bhū - to be'],
    'Verse 23': ['√cal - to move', '√rudh - to obstruct'],
    'Verse 24': ['√yā - to go', '√sthā - to stand'],
    'Verse 25': ['√bhid - to pierce', '√gam - to go'],
    'Verse 26': ['√prāp - to reach', '√sthā - to be situated'],
    'Verse 27': ['√dhyai - to meditate', '√bhū - to become'],
    'Verse 28': ['√vṛt - to turn', '√bhū - to be'],
    'Verse 29': ['√vid - to know', '√jñā - to know'],
    'Verse 30': ['√sidh - to accomplish', '√yā - to go'],
    'Verse 31': ['√pā - to drink', '√bhuj - to enjoy'],
    'Verse 32': ['√kṛ - to do', '√dhṛ - to hold'],
    'Verse 33': ['√bandh - to bind', '√rudh - to restrain'],
    'Verse 34': ['√jap - to repeat', '√dhyai - to meditate'],
    'Verse 35': ['√śru - to hear', '√vac - to speak'],
    'Verse 36': ['√tyaj - to abandon', '√grah - to grasp'],
    'Verse 37': ['√bhū - to be', '√sidh - to accomplish'],
}


def add_roots_to_verse(grammar_cell: str, roots: list) -> str:
    """
    Add roots to a grammar cell that has a summary but no roots.

    Args:
        grammar_cell: The HTML content of the grammar cell
        roots: List of root strings like '√vand - to honor'

    Returns:
        Updated grammar cell with roots added
    """
    # Check if roots already exist
    if '[√' in grammar_cell:
        # Roots already present
        return grammar_cell

    # Check if there's a closing </strong><br> pattern
    if '</strong><br>' in grammar_cell:
        # Add roots after the summary
        root_string = '[' + ', '.join(roots) + ']'
        return grammar_cell.replace('</strong><br>\n', f'</strong><br>\n{root_string}\n')

    return grammar_cell


def process_file():
    """Process the HTML file and add missing roots."""
    input_file = '/Users/mariaiontseva/pasupata-sutra-analysis/index.html'

    print("Reading HTML file...")
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    print("Processing verses...")
    output_lines = []
    i = 0
    verses_updated = 0

    while i < len(lines):
        line = lines[i]
        output_lines.append(line)

        # Look for verse comments
        verse_match = re.search(r'<!-- Verse (\d+)', line)
        if verse_match:
            verse_num = verse_match.group(1)
            verse_key = f'Verse {verse_num}'

            # Look ahead for the grammar cell
            j = i + 1
            while j < min(i + 100, len(lines)):  # Look within next 100 lines
                if '<td class="grammar">' in lines[j]:
                    # Found grammar cell
                    # Check if it needs roots
                    if '<strong>' in lines[j] and '[√' not in lines[j]:
                        # Has summary but no roots
                        if verse_key in VERSE_ROOTS:
                            # Add roots
                            roots = VERSE_ROOTS[verse_key]
                            original_line = lines[j]
                            updated_line = add_roots_to_verse(original_line, roots)

                            if updated_line != original_line:
                                lines[j] = updated_line
                                verses_updated += 1
                                print(f"  Added roots to {verse_key}")
                    break
                j += 1

        i += 1

    print(f"\nUpdated {verses_updated} verse(s)")

    # Write output
    print("Writing updated file...")
    with open(input_file, 'w', encoding='utf-8') as f:
        f.writelines(output_lines if verses_updated == 0 else lines)

    print("Done!")
    return verses_updated


if __name__ == '__main__':
    try:
        updated = process_file()
        sys.exit(0 if updated >= 0 else 1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

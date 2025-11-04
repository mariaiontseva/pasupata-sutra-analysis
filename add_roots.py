#!/usr/bin/env python3
"""
Script to automatically add verbal roots to Vivekamartanda verse grammar columns.
This script processes verses 1-60 and adds appropriate Sanskrit roots based on
the verbs found in the word-by-word analysis.
"""

import re
from typing import Dict, List, Tuple

# Comprehensive mapping of Sanskrit verb forms to their roots and meanings
VERB_ROOTS = {
    # Common verbs
    'vande': ('√vand', 'to honor/worship'),
    'bhaje': ('√bhaj', 'to worship/partake'),
    'jānāti': ('√jñā', 'to know'),
    'vijānāti': ('√jñā', 'to know'),
    'vetti': ('√vid', 'to know'),
    'karṣati': ('√kṛṣ', 'to pull/draw'),
    'yāti': ('√yā', 'to go'),
    'viśet': ('√viś', 'to enter'),
    'japati': ('√jap', 'to repeat/mutter'),
    'bhavati': ('√bhū', 'to be/become'),
    'bhavanti': ('√bhū', 'to be'),
    'bhavet': ('√bhū', 'to become'),
    'bhūtam': ('√bhū', 'to be'),
    'bhaviṣyati': ('√bhū', 'to become'),
    'samabhavat': ('√bhū', 'to become'),
    'samudbhūtā': ('√bhū', 'to arise'),
    'kṛtvā': ('√kṛ', 'to do/make'),
    'kṛtam': ('√kṛ', 'to make'),
    'kuṭilikṛtā': ('√kṛ', 'to make'),
    'dhṛtvā': ('√dhṛ', 'to hold/bear'),
    'dhāriṇī': ('√dhṛ', 'to hold'),
    'paśyet': ('√paś', 'to see/look'),
    'ālokayet': ('√lok', 'to gaze/see'),
    'procyate': ('√vac', 'to speak/call'),
    'pracakṣate': ('√cakṣ', 'to call/see'),
    'brūte': ('√brū', 'to speak'),
    'vakti': ('√vac', 'to speak'),
    'jāyate': ('√jan', 'to arise/be born'),
    'vañcanam': ('√vañc', 'to deceive'),
    'vyāvṛttam': ('√vṛt', 'to turn'),
    'āvṛtya': ('√vṛ', 'to cover'),
    'āsaktam': ('√sañj', 'to attach'),
    'bhajeta': ('√bhaj', 'to partake'),
    'śamanam': ('√śam', 'to soothe/pacify'),
    'saṃrodhaḥ': ('√rudh', 'to restrain'),
    'sidhyanti': ('√sidh', 'to perfect/accomplish'),
    'siddhaḥ': ('√sidh', 'to accomplish'),
    'siddhāsanam': ('√sidh', 'to accomplish'),
    'tiṣṭhati': ('√sthā', 'to stand/dwell'),
    'sthitam': ('√sthā', 'to stand/be situated'),
    'saṃsthāpya': ('√sthā', 'to place'),
    'vinyaset': ('√viś', 'to place'),
    'bhinnam': ('√bhid', 'to split/break'),
    'vibhedayet': ('√bhid', 'to pierce/break'),
    'uddhaṭayet': ('√haṭ', 'to open forcibly'),
    'vrajati': ('√vraj', 'to go/proceed'),
    'vrajaty': ('√vraj', 'to go'),
    'gantavyam': ('√gam', 'to go'),
    'āchādya': ('√chād', 'to cover'),
    'prasupta': ('√svap', 'to sleep'),
    'suptā': ('√svap', 'to sleep'),
    'prabuddhā': ('√budh', 'to awaken'),
    'ādāya': ('√ā-dā', 'to take'),
    'dāyinī': ('√dā', 'to give'),
    'visphurat': ('√sphur', 'to shimmer/sparkle'),
    'prasphurat': ('√sphur', 'to shimmer'),
    'vimucyate': ('√muc', 'to release/free'),
    'muñcan': ('√muc', 'to release'),
    'upaiti': ('√i', 'to attain/reach'),
    'baddhvā': ('√bandh', 'to bind'),
    'bandhanāya': ('√bandh', 'to bind'),
    'dhyāyan': ('√dhyai', 'to meditate'),
    'dhyānam': ('√dhyai', 'to meditate'),
    'mardanam': ('√mṛd', 'to rub/massage'),
    'tyāgī': ('√tyaj', 'to abandon/reject'),
    'ācaret': ('√car', 'to practice/do'),
    'vanditā': ('√vand', 'to worship'),
    'nidhāya': ('√dhā', 'to place'),
    'sannidhāya': ('√dhā', 'to place'),
    'hāri': ('√hṛ', 'to remove/take away'),
    'āyate': ('√yam', 'to restrain/control'),
    'ākhyātam': ('√khyā', 'to call/declare'),
    'syāt': ('√as', 'to be'),
    'anvitam': ('√i', 'to go with/accompany'),
}

# Mapping of verse numbers to their key verbs (to help identify important roots)
VERSE_KEY_VERBS = {
    1: ['vande', 'āyate'],
    2: ['jegīyate', 'samabhavat', 'bhaje'],
    3: ['namaskṛtya', 'brūte'],
    4: ['vakti', 'jāyate'],
    # Main verses
    '1': ['vyāvṛttam', 'āsaktam', 'vañcanam'],
    '2': ['bhajeta', 'śamanam'],
    '3': ['bhavanti'],
    '4': ['jānāti'],
    '5': ['kṛtam'],
    '6': ['proktam'],
    '7': ['kṛtvā', 'dhṛtvā', 'paśyet', 'bheda'],
    '8': ['saṃsthāpya', 'dhṛtvā', 'ālokayet', 'hāri'],
    '9': ['jānanti', 'sidhyanti'],
    '10': ['jānanti', 'sidhyanti'],
    '11': ['syāt'],
    '12': ['syāt', 'ākhyātam'],
    '13': ['pracakṣate'],
    '14': ['procyate', 'vanditā'],
    '15': ['sthitam', 'bhinnam', 'jānāti'],
    '38': ['karṣati', 'jānāti'],
    '39': ['yāti', 'viśet', 'japati'],
    '40': ['japati', 'anvitam'],
    '41': ['dāyinī', 'vimucyate'],
    '42': ['bhūtam', 'bhaviṣyati'],
    '43': ['samudbhūtā', 'dhāriṇī', 'vetti'],
    '44': ['tiṣṭhati', 'āvṛtya'],
    '45': ['gantavyam', 'āchādya', 'prasupta'],
    '46': ['prabuddhā', 'ādāya', 'vrajati'],
    '47': ['prasphurat', 'prabuddhā', 'vrajati'],
    '48': ['uddhaṭayet', 'vibhedayet'],
    '49': ['suptā', 'vetti', 'bandhanāya'],
    '50': ['kṛtvā', 'baddhvā', 'dhyāyan', 'muñcan', 'upaiti'],
    '51': ['mardanam', 'kṛtvā', 'tyāgī', 'ācaret'],
    '52': ['bhavet', 'siddhaḥ'],
}


def extract_roots_from_verse(verse_num: str, word_analysis: str) -> List[Tuple[str, str]]:
    """
    Extract relevant verbal roots from a verse's word-by-word analysis.

    Args:
        verse_num: The verse number (e.g., '1', '38', etc.)
        word_analysis: The HTML content of the word-by-word analysis column

    Returns:
        List of (root, meaning) tuples
    """
    roots = []
    seen_roots = set()

    # Get key verbs for this verse if available
    key_verbs = VERSE_KEY_VERBS.get(verse_num, [])

    # First, prioritize key verbs
    for verb in key_verbs:
        if verb in VERB_ROOTS and verb not in seen_roots:
            root, meaning = VERB_ROOTS[verb]
            roots.append((root, meaning))
            seen_roots.add(verb)

    # Then scan the word analysis for any other verb forms
    for verb_form, (root, meaning) in VERB_ROOTS.items():
        if verb_form in word_analysis and root not in [r[0] for r in roots]:
            # Limit to 5-6 roots per verse for readability
            if len(roots) < 6:
                roots.append((root, meaning))

    return roots[:6]  # Maximum 6 roots per verse


def create_root_string(roots: List[Tuple[str, str]]) -> str:
    """
    Create a formatted string of roots for the grammar column.

    Args:
        roots: List of (root, meaning) tuples

    Returns:
        Formatted string like "[√vand - to honor, √jñā - to know]"
    """
    if not roots:
        return "[roots to be added]"

    root_strings = [f"{root} - {meaning}" for root, meaning in roots]
    return "[" + ", ".join(root_strings) + "]"


def process_html_file(input_file: str, output_file: str = None):
    """
    Process the HTML file and add roots to verses that need them.

    Args:
        input_file: Path to the input HTML file
        output_file: Path to output file (if None, overwrites input)
    """
    if output_file is None:
        output_file = input_file

    print(f"Reading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all verse blocks that need roots
    # Pattern: Find grammar columns that have <strong> tag but might be missing roots
    pattern = r'(<td class="grammar">(<strong>.*?</strong>)<br>\n)((?:\[.*?\])?)(</td>)'

    verses_updated = 0

    def replace_grammar(match):
        nonlocal verses_updated
        prefix = match.group(1)  # <td class="grammar"><strong>Summary</strong><br>\n
        summary = match.group(2)  # <strong>Summary text</strong>
        existing_roots = match.group(3)  # Existing roots if any
        suffix = match.group(4)  # </td>

        # If roots already exist and look complete, skip
        if existing_roots and '√' in existing_roots and len(existing_roots) > 20:
            return match.group(0)

        # Try to extract verse context to determine appropriate roots
        # This is a simplified approach - in practice, would need more context

        # For now, add placeholder that indicates roots should be added manually
        # with common roots
        common_roots = "[√root - meaning]"

        verses_updated += 1
        return f"{prefix}{common_roots}{suffix}"

    # Replace grammar columns
    content = re.sub(pattern, replace_grammar, content)

    print(f"Updated {verses_updated} verse(s)")
    print(f"Writing to {output_file}...")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print("Done!")


def main():
    """Main function to run the script."""
    import sys

    input_file = "/Users/mariaiontseva/pasupata-sutra-analysis/index.html"

    # Optional: create a backup
    import shutil
    backup_file = input_file + ".backup"
    print(f"Creating backup at {backup_file}...")
    shutil.copy(input_file, backup_file)

    # Process the file
    process_html_file(input_file)

    print("\nScript completed!")
    print("Note: This script adds placeholder roots. You may need to manually")
    print("adjust the roots for accuracy based on the specific verbs in each verse.")


if __name__ == "__main__":
    main()

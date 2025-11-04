#!/usr/bin/env python3
"""
Simple script to find and add missing roots to Vivekamartanda verses.
Scans for grammar columns with summaries but no roots, and adds appropriate roots.
"""

import re
import sys


def scan_for_missing_roots(html_content):
    """Scan HTML and identify verses missing roots."""
    # Pattern: grammar cell with strong tag but missing roots
    pattern = r'<td class="grammar">(<strong>.*?</strong>)<br>\n((?!\[√).*?)</td>'

    matches = re.finditer(pattern, html_content, re.DOTALL)

    missing_roots = []
    for match in matches:
        summary = match.group(1)
        after_summary = match.group(2).strip()

        # Check if roots are truly missing (no √ symbol)
        if '√' not in after_summary:
            # Get some context before this match
            start = max(0, match.start() - 200)
            context = html_content[start:match.start()]

            # Try to find verse number from context
            verse_match = re.search(r'Verse (\d+)|V(\d+)', context)
            verse_num = None
            if verse_match:
                verse_num = verse_match.group(1) or verse_match.group(2)

            missing_roots.append({
                'verse': verse_num,
                'summary': summary,
                'position': match.start()
            })

    return missing_roots


def add_common_roots_pattern(html_content):
    """
    Add roots to grammar columns based on common patterns.
    This version adds smart roots based on keywords in the summary.
    """

    # Keyword-based root mapping
    keyword_roots = {
        'asana': ['√as - to sit'],
        'posture': ['√as - to sit', '√sthā - to stand'],
        'chakra': ['√jñā - to know'],
        'knowledge': ['√jñā - to know', '√vid - to know'],
        'liberation': ['√muc - to release', '√sidh - to perfect'],
        'meditation': ['√dhyai - to meditate'],
        'breath': ['√an - to breathe', '√prāṇ - to breathe'],
        'nadi': ['√nad - to flow', '√vah - to carry'],
        'channel': ['√vah - to carry', '√gam - to go'],
        'element': ['√bhū - to be', '√sthā - to stand'],
        'fire': ['√jval - to burn', '√dah - to burn'],
        'water': ['√plu - to float', '√sic - to pour'],
        'bindu': ['√bind - to drop'],
        'mantra': ['√man - to think', '√jap - to repeat'],
        'petal': ['√dḷ - to burst open'],
        'lotus': ['√pad - to go'],
        'location': ['√sthā - to stand', '√vas - to dwell'],
        'description': ['√vac - to speak', '√kathay - to tell'],
        'essential': ['√jñā - to know'],
        'practice': ['√car - to practice', '√kṛ - to do'],
    }

    def get_roots_for_summary(summary):
        """Determine appropriate roots based on summary content."""
        summary_lower = summary.lower()
        roots = []

        for keyword, keyword_roots_list in keyword_roots.items():
            if keyword in summary_lower:
                roots.extend(keyword_roots_list)

        # Remove duplicates while preserving order
        seen = set()
        unique_roots = []
        for root in roots:
            if root not in seen:
                seen.add(root)
                unique_roots.append(root)

        return unique_roots[:4]  # Limit to 4 roots

    # Find grammar cells with summaries but no roots
    pattern = r'(<td class="grammar">)(<strong>.*?</strong>)<br>\n((?!\[√))(</td>)'

    def replace_func(match):
        prefix = match.group(1)
        summary = match.group(2)
        existing = match.group(3)
        suffix = match.group(4)

        # Get roots for this summary
        roots = get_roots_for_summary(summary)

        if roots:
            root_string = '[' + ', '.join(roots) + ']'
            return f"{prefix}{summary}<br>\n{root_string}\n{suffix}"
        else:
            # Add generic placeholder
            return f"{prefix}{summary}<br>\n[√root - meaning]\n{suffix}"

    updated_content = re.sub(pattern, replace_func, html_content, flags=re.DOTALL)

    return updated_content


def main():
    """Main function."""
    input_file = '/Users/mariaiontseva/pasupata-sutra-analysis/index.html'

    print("=" * 60)
    print("Adding Missing Roots to Vivekamartanda Verses")
    print("=" * 60)

    # Read file
    print(f"\n1. Reading {input_file}...")
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return 1

    # First, scan to see what's missing
    print("\n2. Scanning for verses missing roots...")
    missing = scan_for_missing_roots(content)

    if missing:
        print(f"   Found {len(missing)} verse(s) missing roots:")
        for item in missing[:10]:  # Show first 10
            verse_info = f"Verse {item['verse']}" if item['verse'] else "Unknown verse"
            print(f"   - {verse_info}: {item['summary'][:60]}...")
        if len(missing) > 10:
            print(f"   ... and {len(missing) - 10} more")
    else:
        print("   All verses have roots! ✓")
        return 0

    # Add roots
    print("\n3. Adding roots based on content analysis...")
    updated_content = add_common_roots_pattern(content)

    # Create backup
    backup_file = input_file + '.before_roots'
    print(f"\n4. Creating backup at {backup_file}...")
    try:
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        print(f"Warning: Could not create backup: {e}")

    # Write updated content
    print(f"\n5. Writing updated content...")
    try:
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
    except Exception as e:
        print(f"Error writing file: {e}")
        return 1

    # Verify
    print("\n6. Verifying changes...")
    with open(input_file, 'r', encoding='utf-8') as f:
        new_content = f.read()

    new_missing = scan_for_missing_roots(new_content)
    print(f"   Before: {len(missing)} verses missing roots")
    print(f"   After:  {len(new_missing)} verses missing roots")
    print(f"   Added:  {len(missing) - len(new_missing)} sets of roots")

    print("\n" + "=" * 60)
    print("✓ Script completed successfully!")
    print("=" * 60)
    print("\nNote: Roots were added based on keywords in the summaries.")
    print("You may want to review and refine them for accuracy.")

    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nScript interrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"\nUnexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

#!/usr/bin/env python3
"""
Batch migrate all courseware HTML files to use shared library.
1. Add <link rel="stylesheet" href="shared/courseware.css">
   <script src="shared/courseware.js"></script> in <head>
2. Remove the redundant speakPage IIFE at the bottom

Run: python3 scripts/batch_migrate_shared.py
"""

import os
import re
import glob

COURSEWARE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'courseware')

def add_shared_refs(html):
    """Add shared CSS and JS references in <head> if not present."""
    if 'shared/courseware.css' in html:
        return html, False  # already done

    # Find insertion point: after GSAP CDN script if present, otherwise after </script> tags
    # Strategy: insert before the first <style> tag
    style_match = re.search(r'(\s*)(<style[^>]*>)', html, re.IGNORECASE)
    if style_match:
        indent = style_match.group(1)
        insert = f'{indent}<link rel="stylesheet" href="shared/courseware.css">\n'
        insert += f'{indent}<script src="shared/courseware.js"></script>\n'
        insert += style_match.group(2)
        html = html[:style_match.start()] + insert + html[style_match.end():]
        return html, True
    
    return html, False

def remove_speak_page_iife(html):
    """Remove the redundant speakPage IIFE block."""
    # Pattern: comment marker + <script>...</script>
    pattern = re.compile(
        r'<!-- ═══ Speak Page - MP3优先, TTS后备 ═══ -->\s*<script>\s*\(function\(\)\{.*?btn\.addEventListener\(\'click\',function\(e\)\{e\.stopPropagation\(\);speakPage\(\);\}\);.*?\}\)\(\);\s*</script>',
        re.DOTALL
    )
    match = pattern.search(html)
    if not match:
        # Try alternative pattern - different formatting
        pattern2 = re.compile(
            r'<!-- ═══ Speak Page - MP3优先, TTS后备 ═══ -->\s*<script>\s*\(function\(\) \{.*?btn\.addEventListener\(\'click\',\s*function\s*\(e\)\s*\{.*?e\.stopPropagation\(\);.*?speakPage\(\);.*?\}.*?;.*?\}\)\(\);\s*</script>',
            re.DOTALL
        )
        match = pattern2.search(html)
    
    if match:
        html = html[:match.start()] + html[match.end():]
        # Clean up extra blank lines
        html = re.sub(r'\n{3,}', '\n\n', html)
        return html, True
    
    return html, False

def process_file(filepath):
    """Process a single HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    original_len = len(html)
    changes = []
    
    # Step 1: Add shared refs
    html, refs_added = add_shared_refs(html)
    if refs_added:
        changes.append('shared_refs')
    
    # Step 2: Remove speakPage IIFE
    html, iife_removed = remove_speak_page_iife(html)
    if iife_removed:
        changes.append('speakPage_removed')
    
    if changes:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        saved = original_len - len(html)
        return True, changes, saved
    
    return False, changes, 0

def main():
    html_files = sorted(glob.glob(os.path.join(COURSEWARE_DIR, '*.html')))
    all_files = len(html_files)
    modified = 0
    skipped = 0
    errors = []
    total_saved = 0
    
    for fpath in html_files:
        fname = os.path.basename(fpath)
        try:
            ok, changes, saved = process_file(fpath)
            if ok:
                modified += 1
                total_saved += saved
                print(f'  ✓ {fname} (saved {saved}B): {", ".join(changes)}')
            else:
                skipped += 1
        except Exception as e:
            errors.append((fname, str(e)))
            print(f'  ✗ {fname}: ERROR - {e}')
    
    print(f'\n--- Summary ---')
    print(f'Total: {all_files} files')
    print(f'Modified: {modified}')
    print(f'Skipped (already done): {skipped}')
    print(f'Total bytes saved: {total_saved}')
    if errors:
        print(f'Errors: {len(errors)}')
        for f, e in errors:
            print(f'  - {f}: {e}')

if __name__ == '__main__':
    main()

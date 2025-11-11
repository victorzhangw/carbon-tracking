#!/usr/bin/env python3
"""
Script to validate all internal links in markdown files.
Checks if referenced files exist and reports broken links.
"""

import sys
import os
# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import os
import re
from pathlib import Path
from typing import List, Tuple, Dict

def find_all_markdown_files() -> List[Path]:
    """Find all markdown files in the project."""
    md_files = []
    for root, dirs, files in os.walk('.'):
        # Skip certain directories
        skip_dirs = {'.git', 'venv', 'node_modules', '__pycache__', 'backups', 'archive'}
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for file in files:
            if file.endswith('.md'):
                md_files.append(Path(root) / file)
    
    return md_files

def extract_markdown_links(content: str) -> List[Tuple[str, str, int]]:
    """Extract markdown links from content. Returns list of (full_match, link_path, line_number) tuples."""
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    matches = []
    
    lines = content.split('\n')
    for line_num, line in enumerate(lines, 1):
        for match in re.finditer(pattern, line):
            full_match = match.group(0)
            link_path = match.group(2)
            
            # Skip external links and anchors
            if not link_path.startswith(('http://', 'https://', 'mailto:', '#', 'ftp://')):
                matches.append((full_match, link_path, line_num))
    
    return matches

def validate_link(source_file: Path, link_path: str) -> Tuple[bool, str]:
    """Validate if a link points to an existing file. Returns (is_valid, error_message)."""
    # Remove anchor if present
    clean_link = link_path.split('#')[0] if '#' in link_path else link_path
    
    if not clean_link:  # Pure anchor link
        return True, ""
    
    # Resolve relative path
    source_dir = source_file.parent
    target_path = (source_dir / clean_link).resolve()
    
    # Check if file exists
    if target_path.exists():
        return True, ""
    else:
        return False, f"File not found: {target_path}"

def validate_all_links() -> Dict:
    """Validate all links in all markdown files."""
    print("=" * 80)
    print("Validating Internal Links in Markdown Files")
    print("=" * 80)
    print()
    
    # Find all markdown files
    print("Scanning for markdown files...")
    md_files = find_all_markdown_files()
    print(f"Found {len(md_files)} markdown files")
    print()
    
    # Validate links
    print("Validating links...")
    print("-" * 80)
    
    total_links = 0
    broken_links = 0
    files_with_broken_links = 0
    broken_link_details = []
    
    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"⚠️  Error reading {md_file}: {e}")
            continue
        
        links = extract_markdown_links(content)
        if not links:
            continue
        
        file_has_broken_links = False
        file_broken_links = []
        
        for full_match, link_path, line_num in links:
            total_links += 1
            is_valid, error_msg = validate_link(md_file, link_path)
            
            if not is_valid:
                broken_links += 1
                if not file_has_broken_links:
                    file_has_broken_links = True
                    files_with_broken_links += 1
                
                file_broken_links.append({
                    'line': line_num,
                    'link': link_path,
                    'error': error_msg
                })
        
        if file_has_broken_links:
            print(f"\n❌ {md_file}")
            for broken in file_broken_links:
                print(f"   Line {broken['line']}: {broken['link']}")
                print(f"   → {broken['error']}")
            
            broken_link_details.append({
                'file': str(md_file),
                'broken_links': file_broken_links
            })
    
    print()
    print("-" * 80)
    print(f"\nSummary:")
    print(f"  Files scanned: {len(md_files)}")
    print(f"  Total links checked: {total_links}")
    print(f"  Broken links: {broken_links}")
    print(f"  Files with broken links: {files_with_broken_links}")
    print()
    
    if broken_links == 0:
        print("✅ All internal links are valid!")
    else:
        print(f"⚠️  Found {broken_links} broken link(s) in {files_with_broken_links} file(s)")
    
    print()
    print("=" * 80)
    
    return {
        'files_scanned': len(md_files),
        'total_links': total_links,
        'broken_links': broken_links,
        'files_with_broken_links': files_with_broken_links,
        'details': broken_link_details
    }

if __name__ == '__main__':
    result = validate_all_links()
    
    # Exit with error code if broken links found
    if result['broken_links'] > 0:
        exit(1)
    else:
        exit(0)

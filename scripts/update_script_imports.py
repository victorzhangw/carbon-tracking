"""
Update import paths in moved scripts to include project root
"""

import os
import re

# Path setup code to add at the beginning of scripts
PATH_SETUP = """import sys
import os
# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

"""

def update_script_imports(script_path):
    """Add path setup to script if not already present"""
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if path setup already exists
    if 'sys.path.insert' in content:
        print(f"  ✓ {script_path} already has path setup")
        return False
    
    # Find the first import statement
    lines = content.split('\n')
    insert_index = 0
    
    # Skip docstring and comments at the beginning
    in_docstring = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Handle docstrings
        if stripped.startswith('"""') or stripped.startswith("'''"):
            if in_docstring:
                in_docstring = False
                insert_index = i + 1
            else:
                in_docstring = True
            continue
        
        if in_docstring:
            continue
            
        # Skip comments and empty lines
        if stripped.startswith('#') or not stripped:
            continue
        
        # Found first import
        if stripped.startswith('import ') or stripped.startswith('from '):
            insert_index = i
            break
    
    # Insert path setup before first import
    lines.insert(insert_index, PATH_SETUP.rstrip())
    
    # Write back
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"  ✓ Updated {script_path}")
    return True

def main():
    """Update all scripts in scripts/ directory"""
    scripts_dir = 'scripts'
    updated_count = 0
    
    print("\n" + "="*60)
    print("Updating script imports...")
    print("="*60 + "\n")
    
    # Walk through all subdirectories
    for root, dirs, files in os.walk(scripts_dir):
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                script_path = os.path.join(root, file)
                if update_script_imports(script_path):
                    updated_count += 1
    
    print(f"\n✓ Updated {updated_count} scripts")
    print("="*60 + "\n")

if __name__ == '__main__':
    main()

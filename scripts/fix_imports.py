"""
Script untuk fix semua imports dari app.xxx ke relative imports
Run: python scripts/fix_imports.py
"""

import os
import re
from pathlib import Path

# Project root
project_root = Path(__file__).parent.parent
app_dir = project_root / "app"

# Pattern untuk mencari imports
pattern = re.compile(r'^from app\.(.+) import', re.MULTILINE)

def fix_file_imports(file_path: Path) -> bool:
    """Fix imports in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file has app. imports
        if 'from app.' not in content:
            return False
        
        # Replace all app. imports with relative imports
        new_content = pattern.sub(r'from \1 import', content)
        
        if content != new_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✅ Fixed: {file_path.relative_to(project_root)}")
            return True
        
        return False
    
    except Exception as e:
        print(f"❌ Error fixing {file_path}: {e}")
        return False

def main():
    """Main function"""
    print("🔧 Fixing all imports from 'app.xxx' to relative imports...\n")
    
    fixed_count = 0
    total_files = 0
    
    # Scan all Python files in app/
    for py_file in app_dir.rglob("*.py"):
        if py_file.name == '__init__.py':
            continue  # Skip __init__.py files
        
        total_files += 1
        if fix_file_imports(py_file):
            fixed_count += 1
    
    print(f"\n✅ Done! Fixed {fixed_count}/{total_files} files")

if __name__ == "__main__":
    main()

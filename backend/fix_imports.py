"""Fix missing __init__.py files."""
import os
from pathlib import Path

# Directories that need __init__.py
dirs = [
    'config',
    'src',
    'src/core',
    'src/tools',
    'src/vectorstore',
    'src/processing',
    'src/memory',
    'src/utils',
]

for dir_path in dirs:
    init_file = Path(dir_path) / '__init__.py'
    if not init_file.exists():
        init_file.touch()
        print(f"✅ Created {init_file}")
    else:
        print(f"✓ {init_file} already exists")

print("\n✅ All __init__.py files created!")
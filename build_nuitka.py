import os
import subprocess
import sys
from pathlib import Path

ENTRY_POINT = "main.py"
OUTPUT_NAME = "RoboForger"

def build():
    current_dir = Path(os.getcwd())
    resources_dir = os.path.join(current_dir, "RoboForger", "resources")
    
    cmd = [
        sys.executable, "-m", "nuitka",
        "--standalone",          # Create a folder with all dependencies
        # "--onefile",           # one file for single exe
        f"--output-filename={OUTPUT_NAME}",
        "--output-dir=dist",

        "--enable-plugin=pyside6",
        "--windows-disable-console",
        f"--windows-icon-from-ico={os.path.join(resources_dir, 'icon.ico')}",
        
        f"--include-data-dir={resources_dir}=resources",
        
        "--lto=no",              # Link Time Optimization (Set 'yes' for release, 'no' for speed)
        "--jobs=4",              # Use 4 CPU cores

        ENTRY_POINT
    ]

    print("--- Starting Nuitka Build ---")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        subprocess.run(cmd, check=True)
        print("\nBuild Successful!")
        print(f"Artifacts are in: dist/{OUTPUT_NAME}.dist")
    except subprocess.CalledProcessError:
        print("\nBuild Failed")

if __name__ == "__main__":
    if not os.path.exists("pyproject.toml"):
        print("Error: Please run this script from the project root directory.")
        sys.exit(1)
        
    build()
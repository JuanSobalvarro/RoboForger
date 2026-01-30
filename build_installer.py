import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
ISS_SCRIPT = PROJECT_ROOT / "setup_roboforger.iss"

def build_installer():
    print("Building installer using Inno Setup...")
    cmd = [
        "iscc", # ensure to have Inno Setup Compiler in PATH
        str(ISS_SCRIPT)
    ]

    try:
        subprocess.check_call(cmd)
        print("Installer built successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during installer compilation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build_installer()
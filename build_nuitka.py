import os
import subprocess
import sys
from pathlib import Path
import argparse

ENTRY_POINT = "RoboForger/main.py"
OUTPUT_NAME = "RoboForger"

def build(debug=False):
    project_root = Path(__file__).parent
    resources_dir = project_root / "RoboForger" / "resources"
    bin_dir = resources_dir / "bin" / "libredwg"

    cmd = [
        sys.executable, "-m", "nuitka",
        "--standalone",
        f"--output-filename={OUTPUT_NAME}",
        "--output-dir=dist",

        "--enable-plugin=pyside6",
        # TO REMEMBER: qt plugins are the folders from PySide6 library where the dlls
        # are stored. For example, the "platforms" folder contains the "qwindows.dll" file
        # renderers for 3D rendering (opengl)
        # platforms for Windows platform support
        "--include-qt-plugins=renderers,platforms,qml",

        f"--windows-icon-from-ico={resources_dir / 'icon.ico'}",

        f"--include-data-dir={resources_dir}=resources",
        f"--include-data-files={bin_dir / 'dwg2dxf.exe'}=resources/bin/libredwg/dwg2dxf.exe",

        "--nofollow-import-to=typing",
        "--nofollow-import-to=types",
        
        # exclude unittest library if found
        # "--nofollow-import-to=unittest",

        "--msvc=latest",

        "--company-name=JuSo",
        "--product-name=RoboForger",
        "--file-version=2.1.0",

        "--windows-console-mode=disable",

        "--jobs=8",
        "--lto=no" if debug else "--lto=yes",

        ENTRY_POINT
    ]

    if debug:
        cmd += [
            "--debug",
            "--unstripped",
            "--no-debug-immortal-assumptions",
            "--python-flag=-v",
            "--windows-console-mode=force",
        ]

    print("\n--- Starting Nuitka Build ---")
    print(" ".join(cmd))

    subprocess.run(cmd, check=True)

    print("\nBuild successful!")
    print(f"Output: dist/{OUTPUT_NAME}.dist")

if __name__ == "__main__":
    if not Path("pyproject.toml").exists():
        print("Run this script from the project root")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Build RoboForger with Nuitka")
    parser.add_argument("--debug", action="store_true", help="Build in debug mode")
    args = parser.parse_args()

    build(debug=True if args.debug else False)

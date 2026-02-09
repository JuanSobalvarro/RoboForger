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

        # PLUGIN CONTROL
        "--enable-plugin=pyside6",
        # TO REMEMBER: qt plugins are the folders from PySide6 library where the dlls
        # are stored. For example, the "platforms" folder contains the "qwindows.dll" file
        # renderers for 3D rendering (opengl)
        # platforms for Windows platform support
        "--include-qt-plugins=qml,platforms,styles,renderers",

        "--nofollow-import-to=typing",
        "--nofollow-import-to=types",

        # DLLS
        "--noinclude-dlls=qt6charts*",
        "--noinclude-dlls=qt6data*",
        "--noinclude-dlls=qt6lab*",
        "--noinclude-dlls=qt6location*",
        "--noinclude-dlls=qt6multimedia*",
        "--noinclude-dlls=qt6pdf*",
        "--noinclude-dlls=qt6positioning*",
        "--noinclude-dlls=qt6scxml*",
        "--noinclude-dlls=qt6sensors*",
        "--noinclude-dlls=qt6spatial*",
        "--noinclude-dlls=qt6sql*",
        "--noinclude-dlls=qt6test*",
        "--noinclude-dlls=qt6text*",
        "--noinclude-dlls=qt6virtual*",
        "--noinclude-dlls=qt6web*",
        # "--noinclude-dlls=qt6network*",
        # "--noinclude-dlls=qt63d*", # just testing, will also remove 3d from quick
        # "--noinclude-dlls=qt6*",

        # WINDOWS SPECIFIC
        f"--windows-icon-from-ico={resources_dir / 'icon.ico'}",

        # DATA FILES
        f"--include-data-dir={resources_dir}=resources",
        f"--include-data-files={bin_dir / 'dwg2dxf.exe'}=resources/bin/libredwg/dwg2dxf.exe",

        "--msvc=latest",

        # BINARY INFO
        "--company-name=JuSo",
        "--product-name=RoboForger",
        "--file-version=2.1.0",

        "--windows-console-mode=disable",

        "--jobs=8",
        "--lto=no" if debug else "--lto=yes",
    ]

    if debug:
        cmd += [
            "--debug",
            "--unstripped",
            "--no-debug-immortal-assumptions",
            "--python-flag=-v",
            "--windows-console-mode=force",
        ]

    cmd.append(ENTRY_POINT)

    print("\n--- Starting Nuitka Build ---")
    print(f"Debug mode: {'ON' if debug else 'OFF'}")
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

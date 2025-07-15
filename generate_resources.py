import os
import xml.etree.ElementTree as ET
from pathlib import Path
import subprocess

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
QRC_FILE = BASE_DIR / "resources.qrc"
OUTPUT_PY = BASE_DIR / "resources_rc.py"


def generate_qrc():
    qresource = ET.Element("qresource", prefix="/")

    for root, dirs, files in os.walk(ASSETS_DIR):
        for file in files:
            if file.endswith((".svg", ".png", ".jpg", ".jpeg")):
                full_path = Path(root) / file
                relative_path = full_path.relative_to(Path.cwd())
                ET.SubElement(qresource, "file").text = str(relative_path).replace("\\", "/")

    rcc = ET.Element("RCC")
    rcc.append(qresource)

    tree = ET.ElementTree(rcc)
    tree.write(QRC_FILE, encoding="utf-8", xml_declaration=True)
    print(f"✅ Generated: {QRC_FILE}")


def compile_qrc():
    result = subprocess.run(
        ["pyside6-rcc", str(QRC_FILE), "-o", str(OUTPUT_PY)],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"✅ Compiled: {OUTPUT_PY}")
    else:
        print("❌ Error compiling resources:")
        print(result.stderr)


if __name__ == "__main__":
    generate_qrc()
    compile_qrc()

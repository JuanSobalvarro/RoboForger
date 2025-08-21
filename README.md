# RoboForger

RoboForger is a program that can help you with the generation of rapid code given a 
2D dxf file.

## How it works
RoboForger is composed of the Python library `roboforger` and the frontend built with QML and PySide6.

### Compilation
Remember to compile resources running generate_resources.py before running the application.
Test the generation running the `main.py` file. Then compile using `pyinstaller main.spec` to generate the executable.:

```bash
# You can try installer with this
pyinstaller --name RoboForger --workpath build-windows --icon=build-aux/icon.ico --collect-binaries PySide6 --add-data "LICENSE;." --noconsole build/release/main.py --onefile
```
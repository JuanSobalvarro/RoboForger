default:
    @just --list

[group('env')]
check-tools:
    poetry --version
    python --version

[group('env')]
install:
    poetry install

[group('env')]
env-info:
    poetry env info

[group('env')]
check-poetry-active: check-tools
    poetry env activate

[group('run')]
run: check-poetry-active
    python -m RoboForger.main

[group('build')]
build: check-poetry-active
    python build_nuitka.py

[group('build')]
build-debug: check-poetry-active
    python build_nuitka.py --debug

[group('build')]
build-installer: check-poetry-active
    python build_installer.py
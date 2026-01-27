#!/usr/bin/env python
from RoboForger.app.application import RoboforgerApp
import sys
import os


DEBUG = False

def resolve_resource_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # nuitka compiled case
    if "__compiled__" in globals():
        return os.path.join(base_dir, "resources")
    # normal dev/python case
    return os.path.join(base_dir, "RoboForger", "resources")

def main():
    resource_dir = resolve_resource_path()

    if not os.path.exists(resource_dir):
        print(f"Error: Resource directory not found at {resource_dir}")
        sys.exit(1)

    app = RoboforgerApp(sys.argv, resource_dir)

    sys.exit(app.run())


if __name__ == "__main__":
    main()
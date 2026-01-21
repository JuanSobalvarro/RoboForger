#!/usr/bin/env python
from RoboForger.app.application import RoboforgerApp
import sys

DEBUG = False

def main():

    app = RoboforgerApp(sys.argv)

    sys.exit(app.run())


if __name__ == "__main__":
    main()
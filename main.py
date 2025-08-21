#!/usr/bin/env python

DEBUG = False

def main():
    from roboforger_app.startup import perform_startup

    perform_startup(debug=DEBUG)


if __name__ == "__main__":
    main()
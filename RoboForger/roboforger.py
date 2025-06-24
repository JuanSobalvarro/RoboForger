"""
This module provides a CLI for RoboForger.
Example usage:
roboforger -f horse.dxf -o output.txt --offset --use-detector
"""
import argparse

def main():
    arg_parser = argparse.ArgumentParser(description="RoboForger")
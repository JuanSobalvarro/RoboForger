"""
This module creates a Draw class that is used to generate the Rapid Code given a CAD file.
"""
from RoboForger.drawing.draw import Draw


class Forger:
    def __init__(self):

        self.draw = Draw("tool0", 1000)
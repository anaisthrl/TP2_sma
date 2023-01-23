import random

from pygame import Vector2

import core

class Vegetaux:
    def __init__(self):
        self.posXY = Vector2(0,0)  # position des végétaux
        self.size = 0
        self.color = (0,255,0)
        self.estMange = False


    def show(self):
        core.Draw.circle(self.color, self.posXY, self.size)
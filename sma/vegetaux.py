import random

from pygame import Vector2

import core

class Vegetaux:
    def __init__(self):
        self.posXY = Vector2(random.randint(0, core.WINDOW_SIZE[0] - 10),
                         random.randint(0, core.WINDOW_SIZE[1] - 10))  # position des végétaux
        self.size = 5
        self.color = (0,255,0)
        self.estMange = False


    def show(self):
        core.Draw.circle(self.color, self.posXY, self.size)
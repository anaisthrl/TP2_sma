import random

from pygame import Vector2

import core

class Vegetaux:
    def __init__(self):
        self.posXY = Vector2(random.randint(0, core.WINDOW_SIZE[0] - 10),
                         random.randint(0, core.WINDOW_SIZE[1] - 10))  # position des masques
        self.size = 5


    def show(self):
        core.Draw.circle((0,255,0), self.posXY, self.size)
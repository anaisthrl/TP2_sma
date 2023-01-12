import random

from pygame import Vector2

import core
from sma.body import Body
from sma.superpredateur.fustrumSP import FustrumSP


class BodySP(Body):

    def __init__(self):
        Body.__init__(self)
        self.color = (0,0,0)
        self.sizeBody = 30

    def show(self):
        self.color = (255, 0, 0)
        core.Draw.circle(self.color, self.position, self.sizeBody)

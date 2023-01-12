import random

from pygame import Vector2

import core
from sma.body import Body
from sma.superpredateur.fustrumSP import FustrumSP


class BodyH(Body):

    def __init__(self):
        Body.__init__(self)
        self.color = (0,255,0)
        self.sizeBody = 10
        self.esperanceVie = 50
        self.seuilFatigue = 30
        self.seuilFaim = 25


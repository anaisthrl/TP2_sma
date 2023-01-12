import random

from pygame import Vector2

import core
from sma.body import Body
from sma.superpredateur.fustrumSP import FustrumSP


class BodyD(Body):

    def __init__(self):
        Body.__init__(self)
        self.color = (0,0,255)
        self.sizeBody = 10
        self.esperanceVie = 150
        self.seuilFatigue = 50

import random

from pygame import Vector2

import core
from sma.body import Body
from sma.superpredateur.fustrumSP import FustrumSP


class BodyH(Body):

    def __init__(self):
        Body.__init__(self)
        self.color = (187,15,199)
        self.sizeBody = 10
        self.esperanceVie = 400
        self.seuilFatigue = 200
        self.seuilFaim = 25
        self.seuilReproduction = 100


import random

from pygame import Vector2

import core
from sma.body import Body
from sma.superpredateur.fustrumSP import FustrumSP


class BodyH(Body):

    def __init__(self):
        Body.__init__(self)
        self.color = (255,255,0)
        self.sizeBody = 15
        self.esperanceVie = 400
        self.seuilFatigue = 200
        self.seuilFaim = 250
        self.seuilReproduction = 80
        self.seuilRepos = 100


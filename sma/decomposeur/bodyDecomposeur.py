import random

from pygame import Vector2

import core
from sma.body import Body
from sma.superpredateur.fustrumSP import FustrumSP


class BodyD(Body):

    def __init__(self):
        Body.__init__(self)
        self.color = (0,0,255)
        self.sizeBody = 8
        self.esperanceVie = 800
        self.seuilFatigue = 400
        self.seuilFaim = 400
        self.seuilReproduction = 100
        self.seuilRepos = 200

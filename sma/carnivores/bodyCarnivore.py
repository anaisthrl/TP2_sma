import random

from pygame import Vector2

import core
from sma.body import Body
from sma.superpredateur.fustrumSP import FustrumSP


class BodyC(Body):

    def __init__(self):
        Body.__init__(self)
        self.color = (255,100,0)
        self.sizeBody = 20
        self.esperanceVie = 350
        self.seuilFatigue = 200
        self.seuilFaim = 250
        self.seuilReproduction = 150
        self.seuilRepos = 50



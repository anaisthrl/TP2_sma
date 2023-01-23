import random

from pygame import Vector2

import core
from sma.body import Body
from sma.superpredateur.fustrumSP import FustrumSP


class BodySP(Body):

    def __init__(self):
        Body.__init__(self)
        # paramètres pour l'affichage
        self.color = (255, 0, 0)

        # paramètres pour faire avancer le programme
        self.seuilRepos = 50  # temps de repos
        self.estMange = False  # si mangé par le decomposeur

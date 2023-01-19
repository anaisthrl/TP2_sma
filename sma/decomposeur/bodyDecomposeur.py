import random

from pygame import Vector2

import core
from sma.body import Body
from sma.superpredateur.fustrumSP import FustrumSP


class BodyD(Body):

    def __init__(self):
        Body.__init__(self)
        # paramètres pour l'affichage
        self.color = (0,0,255)
        self.sizeBody = 8
        # paramètre spécificiques
        self.velocity = Vector2(random.uniform(-1, 21), random.uniform(-1, 1))  # pour mouvement aléatoire
        self.seuilFaim = 192
        self.esperanceVie = 2220
        self.seuilFatigue = 290
        self.seuilReproduction = 150
        # paramètres pour faire avancer le programme
        self.seuilRepos = 50  # temps de repos
import random

from pygame import Vector2

import core
from sma.body import Body
from sma.superpredateur.fustrumSP import FustrumSP


class BodyH(Body):

    def __init__(self):
        Body.__init__(self)
        # paramètres pour l'affichage
        self.color = (255, 255, 0)
        self.sizeBody = 15
        # paramètre spécificiques
        self.velocity = Vector2(random.uniform(-2.5, 2.5), random.uniform(-2.5, 2.5))  # pour mouvement aléatoire
        self.seuilFaim = 100
        self.esperanceVie = 1110
        self.seuilFatigue = 500
        self.seuilReproduction = 100
        # paramètres pour faire avancer le programme
        self.seuilRepos = 10  # temps de repos
        self.estMange = False  # si mangé par le decomposeur

import random

from pygame import Vector2

import core
from sma.body import Body
from sma.superpredateur.fustrumSP import FustrumSP


class BodyC(Body):

    def __init__(self):
        Body.__init__(self)
        # paramètres pour l'affichage
        self.color = (255,100,0)
        self.sizeBody = 20
        # paramètre spécificiques
        self.velocity = Vector2(random.uniform(-4, 4), random.uniform(-4, 4))  # pour mouvement aléatoire
        self.seuilFaim = 292
        self.seuilFatigue = 300
        self.seuilReproduction = 925
        self.esperanceVie = random.randint(5550, 22200)
        # paramètres pour faire avancer le programme
        self.seuilRepos = 50  # temps de repos
        self.estMange = False  # si mangé par le decomposeur



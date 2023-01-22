from random import random

from pygame import Vector2

from sma.agent import Agent
from sma.carnivores.bodyCarnivore import BodyC
from sma.herbivores.bodyHerbivore import BodyH
from sma.herbivores.herbivore import Herbivore
from sma.superpredateur.bodySP import BodySP


class Carnivore(Agent):

    def __init__(self, body):
        Agent.__init__(self, body)

    def update(self):
        proies, predateurs, congeneres, neighborhood = self.filtrePerception(self.body.fustrum.perceptionList)

        # gestion mangeur - question 6
        proiesDansVision = []
        cible = None

        # gestion survie - question 6
        predateursDansVision = []

        for p in predateurs:
            if not p.estMort: # fuit les superprédateurs
                predateursDansVision.append(p)
                f = self.fuite(predateursDansVision)
                self.body.acceleration += self.body.acceleration - f

        if len(predateursDansVision) == 0:  # mange les herbivores s'il n'est pas entrain de fuire
            for p in proies:
                if not p.estMort :
                    proiesDansVision.append(p)
                    cible = p

                if cible is not None:
                    force = cible.position - self.body.position
                    self.body.acceleration = force
                    if self.body.position.distance_to(cible.position) <= self.body.sizeBody + p.sizeBody:
                        cible.estMort = True
                        self.body.timerFaim = 0

        self.body.update()

    def filtrePerception(self, perceptionList):
        proies = []
        predateurs = []
        congeneres = []
        neighborhood = []
        for p in perceptionList:
            if isinstance(p, BodyH):
                proies.append(p)
            if isinstance(p,BodySP):
                predateurs.append(p)
            if isinstance(p, BodyC):
                congeneres.append(p)
            else:
                neighborhood.append(p)
        return proies, predateurs, congeneres, neighborhood







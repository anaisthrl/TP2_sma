from random import random

from pygame import Vector2

from sma.agent import Agent
from sma.herbivores.bodyHerbivore import BodyH
from sma.herbivores.herbivore import Herbivore
from sma.superpredateur.bodySP import BodySP


class Carnivore(Agent):

    def __init__(self, body):
        Agent.__init__(self, body)

    def update(self):
        proies, predateurs, neighborhood = self.filtrePerception(self.body.fustrum.perceptionList)
        acceleration = Vector2()
        rep = Vector2()
        for n in neighborhood:
            rep = rep + self.body.position - n.position
        att = Vector2()
        for p in proies:
            att = p.position - self.body.position
        for p in predateurs:
            att = p.position - self.body.position
        acceleration = att + rep
        self.body.acceleration = Vector2(0, 0)

        # gestion mangeur - question 6
        proiesDansVision = []
        cible = None

        # gestion survie - question 6
        predateursDansVision = []

        for p in predateurs:
            if not p.estMort: # fuit les superprédateurs
                predateursDansVision.append(p)
                fuite = self.fuite(predateursDansVision)
                self.body.acceleration = self.body.acceleration - fuite

        for p in proies:
            if not p.estMort and len(predateursDansVision) == 0:  # mange les herbivores s'il n'est pas entrain de fuire
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
        neighborhood = []
        for p in perceptionList:
            if isinstance(p, BodyH):
                proies.append(p)
            if isinstance(p,BodySP):
                predateurs.append(p)
            else:
                neighborhood.append(p)
        return proies, predateurs, neighborhood

    def fuite(self, predateurs):
        pilotage = Vector2()
        nbPredateur = 0
        for p in predateurs:
            if self.body.position.distance_to(p.position) != self.body.sizeBody + p.sizeBody:
                diff = p.position - self.body.position
                pilotage += diff
                nbPredateur +=1
            else:
                pilotage += Vector2(random.uniform(-5, 5), random.uniform(-5, 5))
                nbPredateur +=1

        if nbPredateur > 0:
            pilotage /= nbPredateur
            pilotage += self.body.velocity

            if pilotage.length() > self.body.maxAcc:
                pilotage = pilotage.normalize()
                pilotage.scale_to_length(self.body.maxAcc)
        return pilotage



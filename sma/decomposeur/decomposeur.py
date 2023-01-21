from pygame import Vector2

import core
from sma.agent import Agent
from sma.carnivores.bodyCarnivore import BodyC
from sma.carnivores.carnivore import Carnivore
from sma.herbivores.bodyHerbivore import BodyH
from sma.herbivores.herbivore import Herbivore
from sma.superpredateur.bodySP import BodySP
from sma.superpredateur.superpredateur import Superpredateur


class Decomposeur (Agent):

    def __init__(self, body):
        Agent.__init__(self,body)

    def update(self):
        target, neighborhood = self.filtrePerception(self.body.fustrum.perceptionList)
        acceleration = Vector2()
        rep = Vector2()
        for n in neighborhood:
            rep = rep + self.body.position - n.position
        att = Vector2()
        for t in target:
            att = t.position - self.body.position
        acceleration = att + rep
        self.body.acceleration = Vector2(0, 0)

        #gestion mangeur - question 6
        proiesDansVision = []
        cible = None

        for t in target:
            if t.estMort:
                proiesDansVision.append(t)
                cible = t
            if cible is not None:
                force = cible.position - self.body.position
                self.body.acceleration = force
                if self.body.position.distance_to(cible.position) <= self.body.sizeBody+t.sizeBody:
                    cible.estMort = True
                    cible.estMange = True
                    self.body.timerFaim = 0


        self.body.update()


    def filtrePerception(self, perceptionList):
        target = []
        neighborhood = []
        for p in perceptionList:
            if isinstance(p, BodyC) or isinstance(p, BodySP) or isinstance(p, BodyH):
                target.append(p)
            else:
                neighborhood.append(p)
        return target, neighborhood
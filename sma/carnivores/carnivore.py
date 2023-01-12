from pygame import Vector2

from sma.agent import Agent
from sma.herbivores.herbivore import Herbivore


class Carnivore (Agent):

    def __init__(self, body):
        Agent.__init__(self,body)


    def update(self):
        target, neighborhood = self.filtrePerception(self.body.fustrum.perceptionList)
        acceleration = Vector2()
        rep = Vector2()
        for n in neighborhood:
            rep = rep + self.body.position - n.position
        att = Vector2()
        if target is not None:
            att = target.body.position - self.body.position
        acceleration = att + rep
        self.body.acceleration = Vector2(0, 0)

        #gestion mangeur - question 6
        proiesDansVision = []
        cible = None

        for p in neighborhood:
            if not p.estMort:
                proiesDansVision.append(p)
                cible = p
            if cible is not None:
                force = cible.position - self.body.position
                self.body.acceleration = force
                if self.body.position.distance_to(cible.position) <= self.body.sizeBody+p.sizeBody:
                    cible.estMort = True
                    self.body.timerFaim = 0

        self.body.update()


    def filtrePerception(self, perceptionList):
        target = None
        neighborhood = []
        for p in perceptionList:
            if isinstance(p, Herbivore):
                target = p
            else:
                neighborhood.append(p)
        return target, neighborhood
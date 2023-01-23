import random

from pygame import Vector2

from sma.agent import Agent
from sma.carnivores.bodyCarnivore import BodyC
from sma.superpredateur.bodySP import BodySP
from sma.vegetaux import Vegetaux


class Herbivore(Agent):

    def __init__(self, body):
        Agent.__init__(self, body)

    def update(self):
        proies, predateurs, allies, neighborhood = self.filtrePerception(self.body.fustrum.perceptionList)

        # gestion mangeur - question 6
        proiesDansVision = []
        cible = None

        # gestion survie - question 6
        predateursDansVision = []

        for p in predateurs:
            if not p.estMort:
                predateursDansVision.append(p)
                fuite = self.fuite(predateursDansVision)
                self.body.acceleration = self.body.acceleration - fuite
                if len(allies) > 0:
                    self.flock(allies)

        if len(predateursDansVision) == 0:  # mange les végétaux s'il n'est pas entrain de fuire
            for p in proies:
                proiesDansVision.append(p)
                cible = p
                if cible is not None:
                    force = cible.posXY - self.body.position
                    self.body.acceleration = force
                    if self.body.position.distance_to(cible.posXY) <= self.body.sizeBody + p.size:
                        p.estMange = True
                        self.body.timerFaim = 0

        self.body.update()

    def filtrePerception(self, perceptionList):
        proies = []
        predateurs = []
        allies = []
        neighborhood = []
        for p in perceptionList:
            if isinstance(p, Vegetaux):
                proies.append(p)
            if isinstance(p, BodyC):
                predateurs.append(p)
            if isinstance(p, BodySP):
                allies.append(p)
        return proies, predateurs, allies, neighborhood
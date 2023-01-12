
import random

from pygame import Vector2


class Agent:
    def __init__(self, body):
        self.body = body
        self.uuid = random.randint(100000, 999999999)


    def update(self):
        target, neighborhood = self.filter(self.body.fustrum.perceptionList)
        acceleration = Vector2()
        rep = Vector2()
        for n in neighborhood:
            rep = rep + self.body.position - n.position
        att = Vector2()
        if target is not None:
           att = target.body.position - self.body.position
        acceleration = att+rep
        self.body.acceleration = Vector2(0,0)

    def filter(self, perceptionList):
        target = None
        neighborhood = []
        for p in perceptionList:
            if isinstance(p, Agent):
                target = p
            else:
                neighborhood.append(p)
        return target, neighborhood

    def show(self):
        self.body.show()


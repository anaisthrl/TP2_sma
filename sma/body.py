import random

from pygame import Vector2

import core
from fustrum import Fustrum


class Body:
    def __init__(self):
        self.fustrum = Fustrum(100,self)
        self.position = Vector2(random.randint(0, core.WINDOW_SIZE[0]-20), random.randint(0, core.WINDOW_SIZE[1]-20))
        self.velocity = Vector2(random.uniform(-200, 200), random.uniform(-200, 200)) #pour mouvement aléatoire
        self.acceleration = Vector2(random.uniform(-3, 3), random.uniform(-3, 3)) #pour mouvement aléatoire
        self.maxAcc = 3
        self.maxSpeed = 3

    def move(self):
        if self.acceleration.length() > self.maxAcc:
            self.acceleration.scale_to_length(self.maxAcc)

        self.velocity += self.acceleration
        if self.velocity.length() > self.maxSpeed:
            self.velocity.scale_to_length(self.maxSpeed)

        self.position += self.velocity
        self.acceleration = Vector2(0, 0)
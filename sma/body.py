import datetime
import random

from pygame.math import Vector2

import core
from fustrum import Fustrum


class Body:
    def __init__(self):
        self.fustrum = Fustrum(100,self)
        self.position = Vector2(random.randint(0, core.WINDOW_SIZE[0] - 20),
                                random.randint(0, core.WINDOW_SIZE[1] - 20))

        self.position = Vector2(random.randint(0, core.WINDOW_SIZE[0] - 20),
                                random.randint(0, core.WINDOW_SIZE[1] - 20))
        self.velocity = Vector2(random.uniform(-200, 200), random.uniform(-200, 200))  # pour mouvement aléatoire
        self.acceleration = Vector2(random.uniform(-3, 3), random.uniform(-3, 3))  # pour mouvement aléatoire
        self.maxAcc = 3
        self.maxSpeed = 3
        self.seuilFaim = 0
        self.seuilFatigue = 0
        self.seuilReproduction = 0
        self.dateNaissance = datetime.datetime.now()
        self.esperanceVie = 0
        self.sizeBody = 0

        self.timerVie = 0
        self.timerFatigue = 0
        self.estMort = False
        self.dort = False
        self.color = (0,0,0)

    def edge(self):
        if self.position.x <= self.sizeBody:
            self.velocity.x *= -1
            self.acceleration *= -1
        if self.position.x + self.sizeBody >= core.WINDOW_SIZE[0]-18:
            self.velocity.x *= -1
            self.acceleration *= -1
        if self.position.y <= self.sizeBody:
            self.velocity.y *= -1
            self.acceleration *= -1
        if self.position.y + self.sizeBody >= core.WINDOW_SIZE[1]-18:
            self.velocity.y *= -1
            self.acceleration *= -1

    def move(self):
        if not self.dort:
            if not self.estMort : #quand l'agent dort il arrête de bouger
                if self.acceleration.length() > self.maxAcc:
                    self.acceleration.scale_to_length(self.maxAcc)

                self.velocity += self.acceleration
                if self.velocity.length() > self.maxSpeed:
                    self.velocity.scale_to_length(self.maxSpeed)

                self.position += self.velocity
                self.acceleration = Vector2(0, 0)
                self.edge()

    def update(self):
        self.timerVie += 1
        self.timerFatigue += 1
        print(self.timerFatigue)
        print(self.seuilFatigue)
        #gestion esperance vie
        if self.timerVie >= self.esperanceVie:
            self.estMort = True
            self.color = (150,150,150)
        #gestion fatigue
        if self.timerFatigue >= self.seuilFatigue:
            self.dort = True



    def show(self):
        core.Draw.circle(self.color, self.position, self.sizeBody)

import datetime
import random

from pygame.math import Vector2

import core
from fustrum import Fustrum


class Body:
    def __init__(self):
        self.fustrum = Fustrum(250,self)
        self.position = Vector2(random.randint(0, core.WINDOW_SIZE[0] - 20),
                                random.randint(0, core.WINDOW_SIZE[1] - 20))

        self.position = Vector2(random.randint(0, core.WINDOW_SIZE[0] - 20),
                                random.randint(0, core.WINDOW_SIZE[1] - 20))
        self.acceleration = Vector2(random.uniform(-3, 3), random.uniform(-3, 3))  # pour mouvement aléatoire
        self.maxAcc = 3
        self.maxSpeed = 4
        self.dateNaissance = datetime.datetime.now()

        self.timerVie = 0
        self.timerFatigue = 0
        self.timerFaim = 0
        self.timerReproduction = 0
        self.timerDormir = 0
        self.estMort = False
        self.dort = False
        self.reproduction = False
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
                self.edge()
                if self.acceleration.length() > self.maxAcc:
                    self.acceleration.scale_to_length(self.maxAcc)

                self.velocity += self.acceleration
                if self.velocity.length() > self.maxSpeed:
                    self.velocity.scale_to_length(self.maxSpeed)

                self.position += self.velocity
                self.acceleration = Vector2(0, 0)

        if self.dort:
            self.timerDormir += 1
            if self.timerDormir >= self.seuilRepos:
                self.timerFatigue = 0
                self.dort = False
                self.timerDormir = 0


    def update(self):
        if not self.estMort:
            self.timerVie += 1
            self.timerFatigue += 1
            self.timerFaim += 1
            self.timerReproduction += 1

            #gestion esperance vie
            if self.timerVie >= self.esperanceVie:
                self.estMort = True
            #gestion fatigue
            if self.timerFatigue >= self.seuilFatigue/2:
                self.dort = True
            #gestion faim
            if self.timerFaim >= self.seuilFaim:
                self.estMort = True
            #gestion reproduction
            if self.timerReproduction >= self.seuilReproduction:
                self.reproduction = True

    def show(self):
        if self.estMort:
            self.color = (150, 150, 150)
        core.Draw.circle(self.color, self.position, self.sizeBody)

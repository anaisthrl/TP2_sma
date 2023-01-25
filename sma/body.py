import datetime
import random

from pygame.math import Vector2

import core
from fustrum import Fustrum


class Body:
    def __init__(self):
        self.fustrum = Fustrum(300, self)
        self.id = random.randint(1,500)
        self.position = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)
        self.velocity = Vector2(0, 0)
        self.max_speed = 0
        self.max_acc = 0
        self.sizeBody = 0
        self.seuilFaim = 0
        self.seuilFatigue = 0
        self.seuilReproduction = 0
        self.esperanceVie = 0
        self.dateNaissance = datetime.datetime.now()

        # attributs qui vont nous permettre de gérer correctement la simulation
        self.timerVie = 0
        self.timerFatigue = 0
        self.timerFaim = 0
        self.timerReproduction = 0
        self.timerDormir = 0
        self.estMort = False
        self.dort = False
        self.reproduction = False
        self.color = (0,0,0)

    def move(self):
        if not self.dort:
            if not self.estMort : #quand l'agent dort il arrête de bouger
                if self.acceleration.length() > self.max_acc:
                    self.acceleration.scale_to_length(self.max_acc)

                self.velocity += self.acceleration
                if self.velocity.length() > self.max_speed:
                    self.velocity.scale_to_length(self.max_speed)

                prochaine_position = self.position + self.velocity
                prochaine_position.x %= core.WINDOW_SIZE[0]
                prochaine_position.y %= core.WINDOW_SIZE[1]
                self.position = prochaine_position
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

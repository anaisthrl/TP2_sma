
import random

from pygame import Vector2


class Agent:
    def __init__(self, body):
        self.body = body
        self.uuid = random.randint(100000, 999999999)
        self.varCohesion = Vector2()
        self.cohesionFactor = 1.3
        self.alignementFactor = 0.2
        self.separationFactor = 1.3
        self.varSeparation = Vector2()

    def show(self):
        self.body.show()

    # question 6 - fuite & symbiose
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

    def flock(self, bodies):
        agentPerçus = []
        for a in bodies:
            if self.body.position.distance_to(a.position) < self.body.fustrum.rayon:
                if self.body != a:
                    agentPerçus.append(a)
        self.varCohesion =self.cohesion(agentPerçus)*self.cohesionFactor
        al = self.align(agentPerçus) * self.alignementFactor
        self.varSeparation = self.separation(agentPerçus) * -self.separationFactor

        return self.varCohesion, al, self.varSeparation
    def separation(self,bodies):
        steering = Vector2()
        agentsCounter = 0
        for other in bodies:
            if self.body.position.distance_to(other.position) != 0:
                diff = Vector2(other.position.x-self.body.position.x,other.position.y-self.body.position.y)
                if diff.length() > 0.001:
                    diff.scale_to_length(self.body.position.distance_squared_to(other.position))
                    agentsCounter += 1
                    steering += diff
            else:
                steering += Vector2(random.uniform(-5,5),random.uniform(-5,5))
                agentsCounter += 1

        if agentsCounter > 0:
            steering /= agentsCounter

            steering += self.body.velocity

            if steering.length() > self.body.maxAcc:
                steering = steering.normalize()
                steering.scale_to_length(self.body.maxAcc)
        return steering
    def cohesion(self, bodies):
        steering = Vector2()
        agentCounter = 0
        for other in bodies:
            if self.body.position.distance_to(other.position) != 0:
                agentCounter += 1
                steering += other.position

        if agentCounter > 0:
            steering /= agentCounter
            steering -= self.body.position

            steering += self.body.velocity
            if steering.length() > self.body.maxAcc:
                steering = steering.normalize()
                steering.scale_to_length(self.body.maxAcc)

        return steering
    def align(self, bodies):
        steering = Vector2()
        agentCounter = 0
        for other in bodies:
            agentCounter += 1
            steering += other.velocity

        if agentCounter > 0:
            steering /= agentCounter

            steering -= self.body.velocity
            if steering.length() > self.body.maxAcc:
                steering = steering.normalize()
                steering.scale_to_length(self.body.maxAcc)

        return steering
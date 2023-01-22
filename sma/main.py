import random

from pygame import Vector2

import core
from agent import Agent
from body import Body
from sma.carnivores.bodyCarnivore import BodyC
from sma.carnivores.carnivore import Carnivore
from sma.decomposeur.bodyDecomposeur import BodyD
from sma.decomposeur.decomposeur import Decomposeur
from sma.herbivores.bodyHerbivore import BodyH
from sma.herbivores.herbivore import Herbivore
from sma.superpredateur.bodySP import BodySP
from sma.superpredateur.superpredateur import Superpredateur
from sma.vegetaux import Vegetaux


def setup():
    print("Setup START---------")
    core.fps = 30
    core.WINDOW_SIZE = [1000, 600]

    core.memory('agents', [])  # classe mere agent
    core.memory('items', [])

    for i in range(0, 1):
        core.memory('agents').append(Superpredateur(BodySP()))

    for i in range(0, 1):
        core.memory('agents').append(Herbivore(BodyH()))

    for i in range(0, 1):
        core.memory('agents').append(Decomposeur(BodyD()))

    for i in range(0, 1):
        core.memory('agents').append(Carnivore(BodyC()))

    for i in range(0, 1):
        core.memory('items').append(Vegetaux())

    print("Setup END-----------")


def computePerception(a):
    a.body.fustrum.perceptionList = []
    if isinstance(a, Superpredateur) and not a.body.estMort:
        for b in core.memory('agents'):
            if a.body.fustrum.inside(b.body) and not b.body.estMort \
                    and not isinstance(b, Superpredateur) and not isinstance(b, Herbivore) and not isinstance(b, Decomposeur):
                a.body.fustrum.perceptionList.append(b.body)

    if isinstance(a, Carnivore) and not a.body.estMort:
        for b in core.memory('agents'):
            if a.body.fustrum.inside(b.body) and not b.body.estMort:
                a.body.fustrum.perceptionList.append(b.body)

    if isinstance(a, Herbivore) and not a.body.estMort:
        for b in core.memory('items'):
            if a.body.fustrum.insideVege(b):
                a.body.fustrum.perceptionList.append(b)
                if b.estMange:
                    core.memory('items').remove(b)
        for b in core.memory('agents'):
            if a.body.fustrum.inside(b.body) and not b.body.estMort and not isinstance(b, Herbivore):
                a.body.fustrum.perceptionList.append(b.body)

    if isinstance(a, Decomposeur):
        for b in core.memory('agents'):
            if a.body.fustrum.inside(b.body) and b.body.estMort and not isinstance(b, Decomposeur):
                a.body.fustrum.perceptionList.append(b.body)
                if b.body.estMange:
                    core.memory('agents').remove(b)


def computeDecision(a):
    a.update()
    # question 4: gestion de la mort des decomposeurs
    if a.body.estMort and isinstance(a, Decomposeur):
        newVege = Vegetaux()
        newVege.posXY = a.body.position

        core.memory('agents').remove(a)

        core.memory('items').append(newVege)

    # question 4 d: gestion de la reproduction
    if a.body.reproduction and isinstance(a, Superpredateur):
        nbPetit = random.randint(2, 4)
        for i in nbPetit:
            newBody = BodySP()
            newBody.position = a.body.position + Vector2(50, 50)
            core.memory('agents').append(Superpredateur(newBody))
        a.body.reproduction = False
        a.body.timerReproduction = 0

    if a.body.reproduction and isinstance(a, Carnivore):
        newBodyC = BodyC()
        newBodyC.position = a.body.position + Vector2(50, 50)
        core.memory('agents').append(Carnivore(newBodyC))
        a.body.reproduction = False
        a.body.timerReproduction = 0

    if a.body.reproduction and isinstance(a, Herbivore):
        newBodyH = BodyH()
        newBodyH.position = a.body.position + Vector2(50, 50)
        core.memory('agents').append(Herbivore(newBodyH))
        a.body.reproduction = False
        a.body.timerReproduction = 0

    if a.body.reproduction and isinstance(a, Decomposeur):
        newBodyD = BodyD()
        newBodyD.position = a.body.position + Vector2(50, 50)
        core.memory('agents').append(Decomposeur(newBodyD))
        a.body.reproduction = False
        a.body.timerReproduction = 0


def applyDecision(a):
    a.body.move()


def run():
    core.cleanScreen()

    # Display superpredateur
    for agent in core.memory("agents"):
        agent.show()

    for agent in core.memory("agents"):
        computePerception(agent)

    for agent in core.memory("agents"):
        computeDecision(agent)

    for agent in core.memory("agents"):
        applyDecision(agent)

    # display vegetaux
    for item in core.memory("items"):
        item.show()


core.main(setup, run)

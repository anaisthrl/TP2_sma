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

    core.memory('SP', []) #superpredateur
    core.memory('herbivore', [])  # herbivore
    core.memory('decomposeur', [])  # decomposeur
    core.memory('carnivore', [])  # carnivore
    core.memory('vegetaux', [])  # vegetaux

    for i in range(0, 1):
        core.memory('SP').append(Superpredateur(BodySP()))

    for i in range(0,5):
        core.memory('herbivore').append(Herbivore(BodyH()))

    for i in range(0,10):
        core.memory('decomposeur').append(Decomposeur(BodyD()))

    for i in range(0,3):
        core.memory('carnivore').append(Carnivore(BodyC()))

    for i in range(0, 20):
        core.memory('vegetaux').append(Vegetaux())

    print("Setup END-----------")


def computePerception(a):
    a.body.fustrum.perceptionList = []
    if isinstance(a, Superpredateur):
        for b in core.memory('carnivore'):
            if a.body.fustrum.inside(b.body):
                a.body.fustrum.perceptionList.append(b.body)

    if isinstance(a, Herbivore):
        for b in core.memory('vegetaux'):
            if a.body.fustrum.insideVege(b):
                a.body.fustrum.perceptionList.append(b)

    if isinstance(a, Decomposeur):
        for b in core.memory('carnivore'):
            if a.body.fustrum.insideVege(b.body) and b.body.estMort:
                a.body.fustrum.perceptionList.append(b)
        for b in core.memory('herbivore'):
            if a.body.fustrum.insideVege(b.body) and b.body.estMort:
                a.body.fustrum.perceptionList.append(b)
        for b in core.memory('SP'):
            if a.body.fustrum.insideVege(b.body) and b.body.estMort:
                a.body.fustrum.perceptionList.append(b)

    if isinstance(a, Carnivore):
        for b in core.memory('herbivore'):
            if a.body.fustrum.inside(b.body):
                a.body.fustrum.perceptionList.append(b.body)


def computeDecision(a):
    a.update()
    #question 4 d
    if a.body.reproduction and isinstance(a, Superpredateur):
        core.memory('SP').append(Superpredateur(BodySP()))
        a.body.reproduction = False
        a.body.timerReproduction = 0
    if a.body.reproduction and isinstance(a, Carnivore):
        core.memory('carnivore').append(Carnivore(BodyC()))
        a.body.reproduction = False
        a.body.timerReproduction = 0
    if a.body.reproduction and isinstance(a, Herbivore):
        core.memory('herbivore').append(Herbivore(BodyH()))
        a.body.reproduction = False
        a.body.timerReproduction = 0
    if a.body.reproduction and isinstance(a, Decomposeur):
        core.memory('decomposeur').append(Decomposeur(BodyD()))
        a.body.reproduction = False
        a.body.timerReproduction = 0


def applyDecision(a):
    a.body.move()


def run():
    core.cleanScreen()

    # Display superpredateur
    for agent in core.memory("SP"):
        agent.show()

    for agent in core.memory("SP"):
        computePerception(agent)

    for agent in core.memory("SP"):
        computeDecision(agent)

    for agent in core.memory("SP"):
        applyDecision(agent)

    # Display herbivores
    for agent in core.memory("herbivore"):
        agent.show()

    for agent in core.memory("herbivore"):
        computePerception(agent)

    for agent in core.memory("herbivore"):
         computeDecision(agent)

    for agent in core.memory("herbivore"):
        applyDecision(agent)

    # Display decomposeur
    for agent in core.memory("decomposeur"):
        agent.show()

    for agent in core.memory("decomposeur"):
        computePerception(agent)

    for agent in core.memory("decomposeur"):
        computeDecision(agent)

    for agent in core.memory("decomposeur"):
        applyDecision(agent)

    # Display carnivores
    for agent in core.memory("carnivore"):
        agent.show()

    for agent in core.memory("carnivore"):
        computePerception(agent)

    for agent in core.memory("carnivore"):
        computeDecision(agent)

    for agent in core.memory("carnivore"):
        applyDecision(agent)

    #display vegetaux
    for item in core.memory("vegetaux"):
        item.show()


core.main(setup, run)

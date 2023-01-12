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

def setup():
    print("Setup START---------")
    core.fps = 30
    core.WINDOW_SIZE = [1000, 600]

    core.memory('SP', []) #superpredateur
    core.memory('herbivore', [])  # herbivore
    core.memory('decomposeur', [])  # decomposeur
    core.memory('carnivore', [])  # carnivore

    for i in range(0, 1):
        core.memory('SP').append(Superpredateur(BodySP()))

    for i in range(0,10):
        core.memory('herbivore').append(Herbivore(BodyH()))

    for i in range(0,20):
        core.memory('decomposeur').append(Decomposeur(BodyD()))

    for i in range(0,10):
        core.memory('carnivore').append(Carnivore(BodyC()))

    print("Setup END-----------")


def computePerception(a):
    pass


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



core.main(setup, run)

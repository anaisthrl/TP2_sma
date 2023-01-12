import core
from agent import Agent
from body import Body
from sma.superpredateur.bodySP import BodySP
from sma.superpredateur.superpredateur import Superpredateur


def setup():
    print("Setup START---------")
    core.fps = 30
    core.WINDOW_SIZE = [800, 600]

    core.memory('SP', []) #superpredateur

    for i in range(0, 3):
        core.memory('SP').append(Superpredateur(BodySP()))

    print("Setup END-----------")


def computePerception(a):
    pass


def computeDecision(a):
    a.update()


def applyDecision(a):
    a.body.move()


def run():
    core.cleanScreen()

    # Display
    for agent in core.memory("SP"):
        agent.show()

    for agent in core.memory("SP"):
        computePerception(agent)

    for agent in core.memory("SP"):
        computeDecision(agent)

    for agent in core.memory("SP"):
        applyDecision(agent)


core.main(setup, run)

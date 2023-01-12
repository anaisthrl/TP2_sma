import core
from agent import Agent
from body import Body


def setup():
    print("Setup START---------")
    core.fps = 30
    core.WINDOW_SIZE = [800, 600]

    core.memory("agents", [])
    core.memory("item", [])

    for i in range(0, 30):
        core.memory('agents').append(Agent(Body()))

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
    for agent in core.memory("agents"):
        agent.show()

    for item in core.memory("item"):
        item.show()

    for agent in core.memory("agents"):
        computePerception(agent)

    for agent in core.memory("agents"):
        computeDecision(agent)

    for agent in core.memory("agents"):
        applyDecision(agent)


core.main(setup, run)

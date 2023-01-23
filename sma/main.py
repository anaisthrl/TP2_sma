import random
import sys
import threading

import pygame.time
from matplotlib import pyplot as plt
from pygame import Vector2
import core
import json

from sma.carnivores.bodyCarnivore import BodyC
from sma.carnivores.carnivore import Carnivore
from sma.decomposeur.bodyDecomposeur import BodyD
from sma.decomposeur.decomposeur import Decomposeur
from sma.herbivores.bodyHerbivore import BodyH
from sma.herbivores.herbivore import Herbivore
from sma.superpredateur.bodySP import BodySP
from sma.superpredateur.superpredateur import Superpredateur
from sma.vegetaux import Vegetaux

# définition d'une variable globale qui va compter le nombre de frames passées jusqu'à la fin du jeu "duree simulation"
frame_count = 0
duree_simulation = 0
data_json = None

# variables pour l'affichage des statistiques
nb_superpredateurs = 0
nb_carnivores = 0
nb_herbivores = 0
nb_decomposeurs = 0

# variables pour le graphique
temps = []
agents = {"superpredateurs": [], "carnivores": [], "herbivores": [], "decomposeurs": []}

def setup():
    core.memory("last_call", pygame.time.get_ticks())
    print("Setup START---------")
    core.fps = 30
    core.WINDOW_SIZE = [1000, 600]

    core.memory('agents', [])  # classe mere agent
    core.memory('items', [])

    global data_json
    data_json = load("scenario.json")

    for i in range(0, data_json['SuperPredateur']['nb']):
        core.memory('agents').append(Superpredateur(creationBody(data_json, "SuperPredateur")))

    for i in range(0, data_json['Herbivore']['nb']):
        core.memory('agents').append(Herbivore(creationBody(data_json, "Herbivore")))

    for i in range(0, data_json['Decomposeur']['nb']):
        core.memory('agents').append(Decomposeur(creationBody(data_json, "Decomposeur")))

    for i in range(0, data_json['Carnivore']['nb']):
        core.memory('agents').append(Carnivore(creationBody(data_json, "Carnivore")))

    for i in range(0, data_json['Vegetaux']['nb']):
        core.memory('items').append(creationBody(data_json, "Vegetaux"))

    # pour le threading et affichage graphique
    thread = threading.Thread(target=graphique, args=())
    thread.start()

    print("Setup END-----------")


def load(path):
    with open(path) as fichier:
        data = json.load(fichier)
        global duree_simulation
        duree_simulation = data['dureeSimu']

    return data


def creationBody(data, type):
    new_body = None
    if type == "SuperPredateur":
        new_body = BodySP()
    if type == "Carnivore":
        new_body = BodyC()
    if type == "Herbivore":
        new_body = BodyH()
    if type == "Decomposeur":
        new_body = BodyD()
    if type == "Vegetaux" :
        new_body = Vegetaux()

    if type != "Vegetaux":
        new_body.max_speed = data[type]['parametres']['maxSpeed']
        new_body.max_acc = data[type]['parametres']['maxAcc']
        new_body.sizeBody = data[type]['parametres']['sizeBody']
        new_body.seuilFatigue = data[type]['parametres']['maxFatigue']
        new_body.seuilFaim = data[type]['parametres']['maxFaim']
        new_body.seuilReproduction = data[type]['parametres']['maxReproduction']

        new_body.position = Vector2(random.randint(0, core.WINDOW_SIZE[0] - data[type]['parametres']['position'][0]),
                                    random.randint(0, core.WINDOW_SIZE[1] - data[type]['parametres']['position'][1]))
        new_body.velocity = Vector2(random.uniform(-data[type]['parametres']['vitesse'][0], data[type]['parametres']['vitesse'][0]), random.uniform(-data[type]['parametres']['vitesse'][1], data[type]['parametres']['vitesse'][1]))
        new_body.acceleration = Vector2(random.uniform(-data[type]['parametres']['acceleration'][0], data[type]['parametres']['acceleration'][0]), random.uniform(-data[type]['parametres']['acceleration'][1], data[type]['parametres']['acceleration'][1]))

        if type == "SuperPredateur" or type == "Carnivore":
            new_body.esperanceVie = random.randint(data[type]['parametres']['maxTempsVie'][0], data[type]['parametres']['maxTempsVie'][1])
        else:
            new_body.esperanceVie = data[type]['parametres']['maxTempsVie']

    else:
        new_body.posXY = Vector2(random.randint(0, core.WINDOW_SIZE[0] - data[type]['parametres']['posXY'][0]),
                         random.randint(0, core.WINDOW_SIZE[1] - data[type]['parametres']['posXY'][1]))
        new_body.size = data[type]['parametres']['sizeBody']

    return new_body


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
        new_vege = creationBody(data_json,"Vegetaux")
        new_vege.posXY = a.body.position

        core.memory('agents').remove(a)

        core.memory('items').append(new_vege)

    # question 4 d: gestion de la reproduction
    if a.body.reproduction and isinstance(a, Superpredateur):
        nb_petit = random.randint(2, 4)
        for i in nb_petit:
            new_body_sp = creationBody(data_json,"SuperPredateur")
            new_body_sp.position = a.body.position + Vector2(50, 50)
            core.memory('agents').append(Superpredateur(new_body_sp))
        a.body.reproduction = False
        a.body.timerReproduction = 0

    if a.body.reproduction and isinstance(a, Carnivore):
        new_body_c = creationBody(data_json,"Carnivore")
        new_body_c.position = a.body.position + Vector2(50, 50)
        core.memory('agents').append(Carnivore(new_body_c))
        a.body.reproduction = False
        a.body.timerReproduction = 0

    if a.body.reproduction and isinstance(a, Herbivore):
        new_body_h = creationBody(data_json,"Herbivore")
        new_body_h.position = a.body.position + Vector2(50, 50)
        core.memory('agents').append(Herbivore(new_body_h))
        a.body.reproduction = False
        a.body.timerReproduction = 0

    if a.body.reproduction and isinstance(a, Decomposeur):
        new_body_d = creationBody(data_json,"Decomposeur")
        new_body_d.position = a.body.position + Vector2(50, 50)
        core.memory('agents').append(Decomposeur(new_body_d))
        a.body.reproduction = False
        a.body.timerReproduction = 0


def applyDecision(a):
    a.body.move()


def run(last_call=None):
    #gestion du temps de simulation
    global frame_count
    frame_count += 1

    if not (frame_count >= duree_simulation):
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

        calcul_pourcentage()
        calcul_meilleur_individu()
    else: # fin du programme au bout de la durée limite d'exécution
        print("Au final :")
        calcul_pourcentage()
        print("Fin du programme.")
        pygame.quit()
        sys.exit()

def calcul_pourcentage():
    # compte des agents pour l'affichage de pourcentages
    nb_superpredateurs = 0
    nb_carnivores = 0
    nb_herbivores = 0
    nb_decomposeurs = 0

    for agent in core.memory("agents"):
        if not agent.body.estMort:
            if isinstance(agent, Superpredateur):
                nb_superpredateurs += 1
            if isinstance(agent, Carnivore):
                nb_carnivores += 1
            if isinstance(agent, Herbivore):
                nb_herbivores += 1
            if isinstance(agent, Decomposeur):
                nb_decomposeurs += 1

    total = nb_superpredateurs + nb_carnivores + nb_herbivores + nb_decomposeurs
    pourcentageSP = nb_superpredateurs * 100 / total
    pourcentageC = nb_carnivores * 100 / total
    pourcentageH = nb_herbivores * 100 / total
    pourcentageD = nb_decomposeurs * 100 / total
    print("Superprédateurs : " + str(round(pourcentageSP,2)) + " %")
    print("Carnivores: " + str(round(pourcentageC,2)) + " %")
    print("Herbivores : " + str(round(pourcentageH,2)) + " %")
    print("Decomposeurs: " + str(round(pourcentageD,2)) + " %")

def calcul_meilleur_individu():
    meilleur_agent = None
    calcul_temp = 0
    for agent in core.memory("agents"):
        calcul = agent.body.acceleration.x + agent.body.velocity.x + agent.body.seuilFatigue + agent.body.seuilReproduction + agent.body.seuilFatigue
        if calcul_temp < calcul:
            calcul_temp = calcul
            meilleur_agent = agent

    print("L'agent avec la meilleur génétique est : " + str(type(meilleur_agent)) + " avec l'id : " + str(meilleur_agent.body.id) + " qui est né à : " + meilleur_agent.body.dateNaissance.strftime("%H:%M:%S"))

def graphique():
    while True:
        current_time = pygame.time.get_ticks() / 1000
        global temps
        temps.append(current_time)

        agents_temp = {"superpredateurs": 0, "carnivores": 0, "herbivores": 0, "decomposeurs": 0}

        for agent in core.memory("agents"):  # on ne compte pas les agents décédés
            if not agent.body.estMort:
                if isinstance(agent, Superpredateur):
                    agents_temp["superpredateurs"] += 1
                if isinstance(agent, Carnivore):
                    agents_temp["carnivores"] += 1
                if isinstance(agent, Herbivore):
                    agents_temp["herbivores"] += 1
                if isinstance(agent, Decomposeur):
                    agents_temp["decomposeurs"] += 1

        plt.cla()

        global agents
        for key in agents.keys():
            agents[key].append(agents_temp[key])
            if key == "superpredateurs":
                plt.plot(temps, agents[key], 'r', label=key)
            if key == "carnivores":
                plt.plot(temps, agents[key], 'orange', label=key)
            if key == "herbivores":
                plt.plot(temps, agents[key], 'yellow', label=key)
            if key == "decomposeurs":
                plt.plot(temps, agents[key], 'blue', label=key)

        plt.xlabel("Temps (s)")
        plt.ylabel("Nombre d'agents")
        plt.legend(loc="upper center")
        plt.title("Evolution des agents au cours du temps")
        plt.ion()
        plt.draw()
        plt.show()
        plt.pause(0.001)

core.main(setup, run)

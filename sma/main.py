import random

import pygame.time
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

# variable pour l'affichage des statistiques
nb_superpredateurs = 0
nb_carnivores = 0
nb_herbivores = 0
nb_decomposeurs = 0
nb_cadavres = 0

def setup():
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


def run():
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

        for agent in core.memory("agents"):
            if isinstance(agent, Superpredateur):
                global nb_superpredateurs
                nb_superpredateurs += 1
            if isinstance(agent, Carnivore):
                global nb_carnivores
                nb_carnivores += 1
            if isinstance(agent, Herbivore):
                global nb_herbivores
                nb_herbivores += 1
            if isinstance(agent, Decomposeur):
                global nb_decomposeurs
                nb_decomposeurs += 1

        calcul_pourcentage()

def calcul_pourcentage():
    total = nb_superpredateurs + nb_carnivores + nb_herbivores + nb_decomposeurs
    pourcentageSP = nb_superpredateurs * 100 / total
    pourcentageC = nb_carnivores * 100 / total
    pourcentageH = nb_herbivores * 100 / total
    pourcentageD = nb_decomposeurs * 100 / total
    print("Superprédateurs : " + str(pourcentageSP) + "%")
    print("Carnivores: " + str(pourcentageC) + "%")
    print("Herbivores : " + str(pourcentageH) + "%")
    print("Decomposeurs: " + str(pourcentageD) + "%")

core.main(setup, run)

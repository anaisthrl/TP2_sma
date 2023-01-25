# TP2_sma
 
##  POUR LE RENDU

**Rendu TP noté Anaïs THORAL 
5A info apprentissage
POLYTECH LYON**

**Code couleur:**


orange : carnivores


bleu : décomposeurs


jaune : herbivores


rouge: superprédateurs


vert: végétaux


## EXPLICATIONS DU CODE

>Question : 1 Créer l’architecture SMA pour la mise en œuvre d’un vivarium contenant les éléments
précédent (une classe par fichier, un agent doit être pro-actif, avoir un body et un fustrum).

Création de 4 dossiers (carnivores, decomposeur, herbivores, superpredateur) contenant les classes et les body enfants de mes classes mère Agent et Body. J'ai en plus rajouter, pour chaque agent, un fustrum spécifique enfant de Fustrum mais ils ne m'ont pas servi.

>Question 2: Pour chaque élément, ajouter une méthode « show() » pour les afficher
distinctement.

Ma méthode "show()"est initisalisée dans ma classe mère Body. Elle est ensuite appliquée à chaque élément. Elle gère, la représentation de l'agent, ainsi que sa couleur si l'agent est mort.

>Question 3:  Ajouter, pour chaque body: une vitesse, une vitesse max, une accélération max, une jauge de faim, une jauge de fatigue, une jauge de reproduction, une date de naissance et une espérance de vie

Cela a été créé dans la classe mère Body afin que tous mes agents puissent y avoir accès. 

Mes jauges sont représentées comme étant des seuils à ne pas dépasser. Ces seuils sont atteints avec mes compteurs spécifiques (de frames): timerVie, timerFatigue, timerReproduction etc...

>Question 4: Pour chaque body, ajouter une méthode « update() » faisant évoluer les paramètres
précédents en fonction du temps. 
> a: Quand le body est trop vieux, l'agent meurt.

Quand mon timerVie atteint ou dépasse le seuil d'espérance de vie, mon agent décède. Il est alors représenté en gris et sa fonction "move()" est bloquée. 

Si mon agent est un décomposeur il se transforme alors en végétal (géré dans main: computeDecision)

>b: Quand la jauge de fatigue ets pleine, l'agent dort.

Quand mon timerFatigue atteint ou dépasse la moitié de son seuil de fatigue, mon agent dort durant la quantité de son timerDormir. Mon agent s'arrête aussi de bouger.

>c: Quand la jauge de faim est pleine, l'agent meurt de faim

Quand mon timerFaim est atteint ou est supérieur à mon seuil de faim, mon agent meurt.

>d: Quand la jauge de reproduction est pleine, l'agent peut se dédoubler avec une modification aléatoire de ses paramètres

Quand mon timerReproduction est atteint mon agent se reproduit (géré dans le main: computeDecision). Selon la catégorie de l'agent, celui-ci fait un ou plusieurs petits. (voir mes recherches sur l'environnement cohérent).

Concernant la modification aléatoire des paramètres, pour être cohérent avec mes catégories, l'aléatoire sera présent pour la vitesse et l'accélération de mes agents.

Les nouveaux agents naissent près de leur mère et se déplacent préférablement près d'elle.

> Question 5: Pour chaque agent, ajouter une méthode « filtrePerception() »

Chaque "filtrePerception()" est géré dans les classes enfants d'Agent. Chacun de mes agents repèrent leurs proies (s'il y a), leurs prédateurs (s'il y a) ou leurs protecteurs (s'il y a pour la symbiose).

Les "filtrePerception()" utilisent un tableau de perception rempli dans le Fustrum qui est lui-même appelé dans le main (dans computePerception).

> Question 6: Pour chaque agent, ajouter une méthode « update() » pour combiner les
comportements suivants :

>a: "Mangeur": l'agent chasse

- Les superprédateurs chassent les carnivores
- Les carnivores chassent les herbivores
- Les herbivores mangent les végétaux 
- Les décomposeurs mangent les cadavres

Cela est géré dans la méthode "update()" de mes agents, si une proie est dans leurs champs de vision, il la pursuit jusqu'à ce qu'il l'ait mangé.

Son timerFaim est alors remis à 0.

>b: "Survie": l'agent fuit un prédateur

- Les carnivores fuient les superprédateurs
- Les herbivores fuient les carnivores

Cela est aussi géré dans la méthode "update()" de mes agents. La méthode (fuite(): dans Agent) est appelé si un prédateur est dans le champ de vision de la proie. mon agent arrête alors de chasser sa nourriture et se concentre sur sa fuite.

>c: "Symbiose": l'agent utilise un autre agent pour se protéger

- Les herbivores se rapprochent des superPrédateurs afin de ne pas se faire manger par les carnivores (qui ont peur des superPrédateurs). 

J'ai implémenté la fonction "flock()" présente dans Agent. En fonction des différents cohéficients (cohésion, alignement et séparation) nos herbivores se rapprochent des superPrédateurs.

Ce comportement intervient, lorsque nos herbivores sont en fuite et qu'ils ont un superPrédateur dans leur champ de vision.

>Question 7:  Modifier la méthode « update() » de la question 4 pour prendre en compte ses
comportements.

Tout est donc géré dans la méthode "update()" de nos classes enfants d'Agent.

>Question 8: Ajouter un fichier scenario.json contenant les paramètres du vivarium (exemple ici :
https://pastebin.com/bDGhd0D9). Les intervalles [Min, Max] indique un paramètre aléatoire

Vous trouverez mon fichier "scenario.py" à la racine de mon projet. 

Les paramètres présents dans ce fichier sont utilisés dans le Main. 

Vous y retrouverez:

- La durée de la simulation intervient dans la fonction "run()". Le programme s'arrête quand le nombre de frames est atteint. 
- La fonction "creationBody" va gérer toutes les créations de nouveaux agents en fonction des paramètres du fichier.

>Question 9: Ajouter une fonction"load(path)" pour charger un scenario.

Le chargement de mon fichier dans la fonction "load()" de Main

>Question 10: Afficher dans la console le pourcentage de la population

Pour chaque frame, la fonction "calcul_pourcentage()" de Main va être appelé dans le run.

Nous prenons en compte tous les agents qui ne sont pas morts. 

L'affichage se fait en console. Lorsque le programme se ferme automatiquement (durée simulation). Un affichage final se créé. 

>Question 11: Afficher dans la console, l’individu ayant la meilleur génétique (plus grande vitesse
max, plus grandes jauges, etc.)

Cela est affiché à chaque frame et est calculé dans la fonction "calcul_meilleur_individu()". J'ai pris en compte leur accelération, leur vitessage, leur seuil de fatigue, leur seuil de reproduction et leur espérance de vie.

>Question 12: Utiliser matplotlib et threading pour afficher un graphique en temps réel des
populations.

Mon graphique prend en compte les agents toujours vivants.

Dans la fonction "setup()" de Main j'appelle la fonction "graphique()" dans un nouveau thread: 
``thread = threading.Thread(target=graphique, args=())
thread.start()``

Vous retrouverez une courbe en temps réel representation l'évolution de ma population d'agent au cours du temps. Les couleurs associées aux courbes sont les mêmes que celles de mes agents.


## RECHERCHES POUR ENVIRONNEMENTS COHERENT

1 an = 1110 frames (mon programme tourne à 30 frames/secondes)

* Super prédateurs 


Vitesse du Hibou : entre 10 et 20 miles de l'heure 


Couvée du Hibou : 2 à 4 oeufs par an


Espérance de vie : entre 5 et 20 ans 


* Herbivores

Vitesse de la souris: 6 km/h

Reproduction souris : 10 portée / an de 5 à 10 souriceaux

Espérance de vie : 2 ans


Pour les autres agents, le programme tourne à 1 ou deux petits par années.

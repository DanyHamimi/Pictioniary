# piction-IA-ry

## Introduction générale

Le but de notre projet sera de réaliser un "jeu" multijoueur jouable uniquement via la caméra
principalement avec les doigts et où le but sera de dessiner des mots donnés qui seront ensuite 
devinés par l'ia qui sera donc un réseau de neuronnes entraîné à reconnaître ces dessins là.
 

## Objectifs

_Quel est l'objectif principal du projet ?_
L'objectif sera donc d'analyser ce qui est affiché sur la webcam de l'utilisateur,
reconnaitre sa main, et à partir de cela reconnaitre quels doigts
sont levés ou non... à partir de celà dessiner le mot donné pour que l'ia puisse à 
chaque nouveau trait essayer de deviner le dessin.

Dans un premier temps nous devrons travailler sur l'aspect dessin avec la main, utilisation de l'application avec la main,
dessiner, recommencer...

Une fois ces données traitées il faudra les envoyer à l'IA afin qu'elle essaye de deviner le dessin et retourne s'il s'agit
ou non du bon dessin.

Le gameplay du jeu se fera donc en réseau avec d'autre utilisateurs munis d'une webcam et les fera s'affronter sur celui qui fait 
deviner à l'IA le plus de dessins possible en un laps de temps.

_Une fois cet objectif réalisé, quels objectifs secondaires peuvent être
développés ?_

Une fois l'objectif réalisé il sera possible d'ajouter des fonctionnalités 
supplémentaires comme d'autres mini-jeux en utilisants ces fonctionnalités ou en implémentant d'autres fonctionnalités comme la reconnaissance
du visage et des jeux avec celui-ci.
## Testabilité

Si le projet final est "bien" réalisé, il sera possible de jouer à plusieurs utilisateurs et donc de déssiner chacun de son côté en voyant en temps
réel les dessins des autres utilisateurs et le nombre de points qu'ils ont. L'IA sera quant à elle capable de reconnaître avec un taux de précision haut 
ces dessins et donc dire au joueur s'il a effectué ou nom le bon dessin.

## Calendrier

_Quelles sont les grandes étapes du projet, et à quelles dates (approximatives)
devraient elles être atteintes ?_

- Fin janvier : Avoir une IA entrainée à reconnaître certains dessins basique (bateau, moulin...); perfectionner dessin avec main (dessin continu, gomme, commande evaluation)

- Fin février : Reconnaissance en temps réel de ces dessins et amélioration à chaque dessin reconnu.

- jusqu'à Mai : Mise en place du jeu pour jouer en multijoueur, dessiner.


## Références

_Donner éventuellement des liens vers des ressources permettant de comprendre le
sujet, ou à étudier pour bien le commencer_

OpenCV pour analyser les images (en Python/C++)
Mediapipe


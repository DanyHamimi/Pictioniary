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

Dans un premier temps nous devrons travailler sur le fait de capturer les zones
nécessaires à l'analyse (la main, le visage..) et uniquement cela.

Une fois les images capturées analyser en temps réel celles-ci afin de savoir
ce qu'il se passe sur la caméra actuellement.

Finalement faire un "jeu" qui prendra les données retournées par ce qui a été 
analysé par la caméra et qui utilisera celles-ci comme élément de gameplay.

_Une fois cet objectif réalisé, quels objectifs secondaires peuvent être
développés ?_

Une fois l'objectif réalisé il sera possible d'ajouter des fonctionnalités 
supplémentaires en analysant par exemple d'autres parties du corps et permettre au joueur
de jouer avec celles-ci.

## Testabilité

Si le projet final est "bien" réalisé il sera reconnaître les dessins effectués si
ceux-ci son corrects et s'améliorera au fur et à mesure de son utilisation.

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


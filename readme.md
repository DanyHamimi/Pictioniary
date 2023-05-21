# Projet de programmation avancée

# PictionIAry

## Requirements

Pour pouvoir executer le programme il faut avoir

- Python 3.9.6 et pip 23.1.2 Java 19 (Pour macOS silicon)
- Python 3.7.9 et pip 23.1.2 Java 19 (Pour Windows)

## Installation

Si vous êtes sous macos(silicon) et que vous souhaitez installer les dépendances
faites la commande suivante dans le terminal

```bash
pip install -r dependencies/RequireMacSilicon1;pip install -r dependencies/RequireMacSilicon2
```

Si vous êtes sous windows et que vous souhaitez installer les dépendances

faites la commande suivante dans le terminal

```bash
pip install -r dependencies/RequireWindows
```

## Lancement de l'application

Une fois ces commandes effectuées vous pouvez lancer le jeu via le fichier menu.py en faisant

```bash
python3 menu.py
```

Ou bien si votre commande pour executer python est python

```bash
python menu.py
```

Si vous souhaitez démarer un serveur pour pouvoir
host des parties en ligne vous pouvez faire

```bash
javac VideoServer.java;java VideoServer
```

Le serveur sera ensuite lancé sur le port 8080 de la machine ayant lancé le serveur

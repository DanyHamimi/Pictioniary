import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
import pygame
import threading
import random
import sys
import io
import socket
import time
import struct


# Charger l'image de fond
background = pygame.image.load("Imgs/testfond.png")

# Coordonnées temporaires de l'extrémité précédente de la ligne
tmpcordX = -1
tmpcordY = -1

# Indicateur du statut de jeu
inGame = True

# Images capturées depuis la webcam
imageFrame = None
byteFrame = None

# Nom d'utilisateur
username = None

# Index de l'utilisateur dans le service
servIndexUser = None

# Variable d'état de jeu
ingame = None

# Indicateur de présence de deux mains
has2Hands = False

# Liste des noms d'objets pour le jeu Pictionary
objet_names = [
    "POMME", "ECLAIR", "AVION", "SEAU", "CHAPEAU", "ENVELOPPE", "CAROTTE", "HACHE",
    "CUILLERE", "CHAT", "PORTE", "ENCLUME", "FLEUR", "BUS", "MAIN", "POISSON", "LUNETTES", "PAPILLON",
    "NUAGE", "TRIANGLE", "SHORTS"
]

# Valeur trouvée lors du jeu
valFinded = -2

# Valeur à trouver lors du jeu
valToFind = -1

# Charger les données MNIST (base de données de chiffres manuscrits)
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = (
    x_train, y_train), (x_test, y_test) = mnist.load_data()

# Normaliser les données d'entraînement et de test
x_train = tf.keras.utils.normalize(x_train, axis=1)
x_test = tf.keras.utils.normalize(x_test, axis=1)

# Charger les modèles pour la reconnaissance de chiffres, lettres et dessins
model = tf.keras.models.load_model('models/number.model')
modelLetters = tf.keras.models.load_model('models/emnist_letters.h5')
modelDraw = tf.keras.models.load_model('models/DrawModele.h5')

# Initialiser la capture vidéo depuis la webcam
cap = cv2.VideoCapture(0)

# Définir la résolution de la capture vidéo
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Lecture initiale de la webcam pour obtenir la première image
r, frame = cap.read()

# Temps précédent pour le calcul du FPS (images par seconde)
pTime = 0

# Coordonnées temporaires de l'extrémité précédente de la ligne
tmpcordX = -1
tmpcordY = -1

# Initialisation de la détection de mains avec Mediapipe
mpHands = mp.solutions.hands
hands = mpHands.Hands()

# Initialisation de l'outil de dessin avec Mediapipe
mpDraw = mp.solutions.drawing_utils

# Indicateur d'effacement du dessin
Erase = True

# Indicateur de mode de position
Position = False

# Canvas pour enregistrer l'image à sauvegarder
canvasToSave = np.zeros((480, 640, 3), np.uint8)
canvasToSave[:] = 255, 255, 255

# Canvas pour le dessin en cours
canvas = np.zeros((480, 640, 3), np.uint8)

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre du jeu
width, height = 1280, 720
pygame.display.set_mode((width, height))
pygame.display.set_caption("PictionIAry")
window = pygame.display.get_surface()

# Charger l'image de fond dans la fenêtre du jeu
background = pygame.image.load("Imgs/testfond.png")
window.blit(background, (0, 0))

# Polices de texte
font = pygame.font.Font('freesansbold.ttf', 32)
fontsmaller = pygame.font.Font('freesansbold.ttf', 25)

# Chargement des boutons du jeu
but2FindBis = pygame.image.load("Imgs/testbuttondany.png")
butFindedBis = pygame.image.load("Imgs/testbuttondany.png")
butTimerBis = pygame.image.load("Imgs/testbuttondany.png")

# Redimensionnement des boutons du jeu
buttonVal2Find = pygame.transform.scale(but2FindBis, (500, 70))
buttonValFinded = pygame.transform.scale(butFindedBis, (500, 70))
butTimer = pygame.transform.scale(butTimerBis, (200, 80))


has2Hands = False  # Indique si deux mains sont détectées
global score  # Score du joueur
valToFind = "0"  # Valeur à trouver (mot, résultat mathématique, etc.)
AmountPlayer = 0  # Nombre de joueurs
# Modèle à utiliser pour la prédiction (Pictionary, Mots, Mathématiques)
currentModel = None
current_letter_index = None  # Index de la lettre actuelle trouvée dans le mot
letters_found = None  # Lettres déjà trouvées dans le mot

ListPlayers = []  # Liste des identifiants des joueurs

# Police pour l'affichage du mot à trouver
fontMOT = pygame.font.Font('freesansbold.ttf', 60)
stop_flag = threading.Event()  # Drapeau pour arrêter les threads
isEndend = 0  # Indique si la partie est terminée
Online = 0  # Indique si le jeu est en ligne (0 = hors ligne, 1 = en ligne)
typeGa = ""  # Type de jeu ("Pictionary", "Mots" ou "Mathématiques")
back_text = font.render("Quitter", True, (255, 255, 255)
                        )  # Texte du bouton "Quitter"
back_button_width = 150  # Largeur du bouton "Quitter"
back_button_height = 50  # Hauteur du bouton "Quitter"
back_button_x = 50  # Position en x du bouton "Quitter"
back_button_y = 650  # Position en y du bouton "Quitter"
back_button = pygame.Rect(back_button_x, back_button_y, back_button_width,
                          back_button_height)  # Zone du bouton "Quitter"


canvasPlayer2 = np.zeros((480, 640, 3), np.uint8)
canvasPlayer2[:] = 255, 255, 255
player2Surface = pygame.surfarray.make_surface(canvasPlayer2)


def init(gameType):
    """
    Initialiser l'affichage du jeu en fonction du type de jeu.

    Arguments:
        gameType (str): Type de jeu ('Solo', 'Pictionary', 'Mots', 'Mathématiques').
    """
    window.blit(background, (0, 0))
    canvasRecived = np.zeros((350, 350, 3), np.uint8)
    canvasRecived[:] = 255, 255, 255
    if (gameType == "Solo"):
        window.blit(butTimer, (1280 - 200, 720 - 100))


def setNewValue(gameType, valToFind):
    """
    Afficher la valeur à trouver dans le jeu.

    Arguments:
        gameType (str): Type de jeu ('Pictionary', 'Mots', 'Mathématiques').
        valToFind (int): Valeur à trouver.
    """
    textVars = ""
    if (gameType == "Pictionary"):
        textVars = "Dessin à faire : "
    elif (gameType == "Mots"):
        textVars = "Mot à écrire : "
    elif (gameType == "Mathématiques"):
        textVars = "Calcul à faire : "
    window.blit(buttonVal2Find, (750, 50))
    window.blit(buttonValFinded, (750, 150))

    textNb = fontsmaller.render(
        textVars + str(valToFind), True, (255, 255, 255))
    window.blit(textNb, (825, 65))

    textVal = fontsmaller.render("?", True, (255, 255, 255))
    window.blit(textVal, (825, 165))

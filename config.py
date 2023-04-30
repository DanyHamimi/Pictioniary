import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
import pygame


has2Hands = False
objet_names = ["POMME", "LIVRE", "ECLAIR", "SERPENT", "LA TOUR EIFFEL", "BANANE", "AVION", "SEAU", "ENVELOPPE", "CAROTTE", "HACHE", "REVEIL", "CHAT", "ENCUME", "FLEUR", "MAIN", "LUNETTES", "PAPILLON", "TRIANGLE", "SHORTS"]


valFinded = -2
valToFind = -1
# Create an AITrain object
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = (x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = tf.keras.utils.normalize(x_train, axis=1)
x_test = tf.keras.utils.normalize(x_test, axis=1)
model = tf.keras.models.load_model('number.model')
#modelBis = tf.keras.models.load_model('mnist.h5')
modelLetters = tf.keras.models.load_model('emnist_letters.h5')
modelDraw = tf.keras.models.load_model('DrawModele.h5')

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

r, frame = cap.read()
pTime = 0
tmpcordX = -1
tmpcordY = -1
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
Erase = True
Position = False

canvasToSave = np.zeros((480, 640, 3), np.uint8)
canvasToSave[:] = 255, 255, 255

canvas = np.zeros((480, 640, 3), np.uint8)

pygame.init()
width, height = 1280, 720
pygame.display.set_mode((width, height))
pygame.display.set_caption("PictionIAry")
window = pygame.display.get_surface()

background = pygame.image.load("Imgs/testfond.png")
window.blit(background, (0, 0))
font = pygame.font.Font('freesansbold.ttf', 32)
fontsmaller = pygame.font.Font('freesansbold.ttf', 25)
but2FindBis = pygame.image.load("Imgs/testbuttondany.png")
butFindedBis = pygame.image.load("Imgs/testbuttondany.png")
butTimerBis = pygame.image.load("Imgs/testbuttondany.png")

buttonVal2Find = pygame.transform.scale(but2FindBis, (500, 70))
buttonValFinded = pygame.transform.scale(butFindedBis, (500, 70))
butTimer = pygame.transform.scale(butTimerBis, (200, 80))


    #Add buttons to the window

def init(gameType):
    window.blit(background, (0, 0))
    canvasRecived = np.zeros((350, 350, 3), np.uint8)
    canvasRecived[:] = 255, 255, 255
    if(gameType == "Solo"):
        window.blit(butTimer, (1280 - 200, 720 - 100))


def setNewValue(gameType,valToFind):
    textVars = ""
    if(gameType == "Pictionary"):
        textVars = "Dessin à faire : "
        textVars2 = "Dessin trouvé : "
    elif(gameType == "Mots"):
        textVars = "Mot à écrire : "
        textVars2 = "Derniere lettre écrite : "
    elif(gameType == "Mathématiques"):
        textVars = "Calcul à faire : "
        textVars2 = "Résultat trouvé : "
    window.blit(buttonVal2Find, (750, 50))
    window.blit(buttonValFinded, (750, 150))

    textNb = fontsmaller.render(textVars + str(valToFind), True, (255, 255, 255))
    window.blit(textNb, (825, 65))

    textVal = fontsmaller.render(textVars2 + str(0), True, (255, 255, 255))
    window.blit(textVal, (825, 165))




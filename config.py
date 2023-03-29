import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
import pygame


has2Hands = False


valFinded = -2
# Create an AITrain object
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = (x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = tf.keras.utils.normalize(x_train, axis=1)
x_test = tf.keras.utils.normalize(x_test, axis=1)
model = tf.keras.models.load_model('number.model')
modelBis = tf.keras.models.load_model('mnist.h5')

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


def init():

    valToFind = np.random.randint(0, 9)
    print(valToFind)
    window.blit(background, (0, 0))

    textNb = font.render("Chiffre à trouver : " + str(valToFind), True, (255, 255, 255))
    window.blit(textNb, (800, 50))

    textVal = font.render("Chiffre trouvé : " + str(0), True, (255, 255, 255))
    window.blit(textVal, (800, 100))

    draw = pygame.image.load("Imgs/guess.png")
    window.blit(draw, (0, 480))

    canvasRecived = np.zeros((350, 350, 3), np.uint8)
    canvasRecived[:] = 255, 255, 255

    return valToFind


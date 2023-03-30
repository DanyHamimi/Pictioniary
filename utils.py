import cv2
import numpy as np
import pygame
from PIL import Image
import tensorflow as tf
from PIL import ImageOps

from config import *


def drawLine(a, b, tmpcordX, tmpcordY):
    if tmpcordX == -1 and tmpcordY == -1:
        tmpcordX = a
        tmpcordY = b

    cv2.line(canvas, (tmpcordX, tmpcordY), (a, b), (255, 255, 255), 25)
    cv2.line(canvasToSave, (tmpcordX, tmpcordY), (a, b), (0, 0, 0), 25)
    # cv2.imshow("Canvas", canvas)
    tmpcordX = a
    tmpcordY = b
<<<<<<< HEAD
    #Resize the canvas to 350x350
    #canvasBis = cv2.resize(canvas, (350, 350))
=======
    # Resize the canvas to 350x350
    # canvasBis = cv2.resize(canvas, (350, 350))
>>>>>>> 035cfac4469d7a82b41c0731f766db020b04d2f5
    cv2.imwrite("Imgs/canvasBis.jpg", canvasToSave)
    img = Image.open("Imgs/canvasBis.jpg")
    img = img.crop((200, 50, 550, 400))
    img.resize((350, 350))
    img.save("Imgs/canvas.jpg")
    


def imagePrediction():
    imgBis = cv2.imread("Imgs/canvas.jpg")[:, :, 0]
    width = 28
    height = 28
    dim = (width, height)
    imgBis = cv2.resize(imgBis, dim, interpolation=cv2.INTER_AREA)
    imgBis = np.invert(np.array([imgBis]))
    prediction = modelBis.predict([imgBis])[0]
    return np.argmax(prediction)
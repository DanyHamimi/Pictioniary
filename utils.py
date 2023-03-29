import cv2
import numpy as np
import pygame
from PIL import Image
import tensorflow as tf

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
    cv2.imwrite("Imgs/canvas.jpg", canvasToSave)
    # create an image from the area (150, 50), (450, 350) of the canvas and save it in the folder
    img = Image.open("Imgs/canvas.jpg")
    # CROP area of the rectangle (100, 50, 450, 30)
    img = img.crop((200, 50, 550, 400))
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

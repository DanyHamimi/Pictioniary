import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
import pygame
from PIL import Image
import socket
import struct
import time
import threading
import io

from config import *
from utils import drawLine, imagePrediction, preprocess_image,predict

background = pygame.image.load("Imgs/testfond.png")
tmpcordX = -1
tmpcordY = -1
inGame = True
valFinded
imageFrame = None
byteFrame = None
username = None
servIndexUser = None
ingame = None

def win(type):
    window.fill((255, 255, 255))
    window.blit(background, (0, 0))
    font = pygame.font.SysFont('Arial', 100)
    if(type == "online"):
        text = font.render("Tu as gagné", True, (255, 255, 255))
    else:
        text = font.render("Partie terminée, Score :" + type, True, (255, 255, 255))
    text_rect = text.get_rect(center=(1280 // 2, 720 // 2))
    window.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(1000)



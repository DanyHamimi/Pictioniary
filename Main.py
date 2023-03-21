import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
import pygame
from PIL import Image
from AITrain.numRec import *

from config import *
from utils import drawLine, imagePrediction

while True:

    # Update the display
    pygame.display.update()

    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    # ... Reste du code principal ...


    # Put a rectangle on the canvas to draw on it at the middle of it (res is 640x480)
    cv2.rectangle(img, (100, 50), (450, 400), (0, 255, 0), 2)
    if results.multi_hand_landmarks and len(results.multi_hand_landmarks) == 2 and has2Hands == False:
        has2Hands = True
        if has2Hands:
            print("2 mains détectées")

    if results.multi_hand_landmarks and len(results.multi_hand_landmarks) == 1:  # Now detect only one hand
        has2Hands = False
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                if id == 4:
                    tmpx4 = cx
                    tmpy4 = cy
                if id == 19:
                    tmpx19 = cx
                    tmpy19 = cy
                if id == 20:
                    tmpx20 = cx
                    tmpy20 = cy
                if id == 7:
                    tmpx7 = cx
                    tmpy7 = cy
                if id == 15:
                    tmpx15 = cx
                    tmpy15 = cy
                if id == 16:
                    tmpx16 = cx
                    tmpy16 = cy
                if id == 11:
                    tmpx11 = cx
                    tmpy11 = cy
                if id == 12:
                    tmpx12 = cx
                    tmpy12 = cy
                if id == 5:
                    tmpx5 = cx
                    tmpy5 = cy
                if id == 8:
                    # print("Coords de 8", cx, cy)
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                    tmpx8 = cx
                    tmpy8 = cy
            if tmpx19 != 0 and tmpy19 != 0 and tmpx20 != 0 and tmpy20 != 0 and tmpx11 != 0 and tmpy11 != 0 and tmpx12 != 0 and tmpy12 != 0 and tmpx15 != 0 and tmpy15 != 0 and tmpx16 != 0 and tmpy16 != 0 and tmpx4 != 0 and tmpy4 != 0 and tmpx8 != 0 and tmpy8 != 0 and tmpy5 != 0:
                if tmpy5 < tmpy8:
                    if tmpy19 < tmpy20 and tmpy11 < tmpy12 and tmpy15 < tmpy16:
                        canvasToSave[:] = 255, 255, 255
                        canvas[:] = 0, 0, 0
                        tmpcordX = -1  # Ajoutez cette ligne
                        tmpcordY = -1  # Ajoutez cette ligne
                    tmpcordX = -1
                    tmpcordY = -1
                    # print("Doigt Baissé")
                elif tmpy19 > tmpy20 and tmpy11 > tmpy12 and tmpy15 > tmpy16 and tmpy4 > tmpy8 and isTesting == False:
                    # Check if all fingers are up
                    isTesting = True
                    print("photo")
                    try:
                        valFinded = imagePrediction()
                        print(valFinded)
                        textVal = font.render("Chiffre trouvé : " + str(valFinded), True, (0, 0, 0))
                        window.blit(textVal, (800, 100))
                        if valToFind == valFinded:
                            score += 1
                            textNb = font.render("Chiffre à trouver : " + str(valToFind), True, (255, 255, 255))
                            window.blit(textNb, (800, 50))
                            valToFind = np.random.randint(0, 9)
                            textNb = font.render("Chiffre à trouver : " + str(valToFind), True, (0, 0, 0))
                            window.blit(textNb, (800, 50))
                            valFinded = -2
                    except:
                        print("error")
                else:
                    tmpx8 = 640 - tmpx8
                    isTesting = False
                    drawLine(tmpx8, tmpy8)

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    else:
        tmpcordX = -1
        tmpcordY = -1
    img = cv2.flip(img, 1)
    # cv2.imshow("Image", img)
    cv2.addWeighted(canvas, 1, img, 1, 1, img)
    # cv2.imshow("Image", img)
    cv2.waitKey(1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Convert the frame to a Pygame surface
    frame = imgRGB
    frame = np.rot90(frame)

    # add canvasToSave NDArray[uint8] to the window

    frame = pygame.surfarray.make_surface(frame)
    frameCanvas = pygame.surfarray.make_surface(img)
    # Rotate the frame 90 degrees
    frameCanvas = pygame.transform.rotate(frameCanvas, 90)

    frameCanvas = pygame.transform.flip(frameCanvas, False, True)

    # put a white background to the window

    # window.blit(frame, (0, 0))
    window.blit(frameCanvas, (0, 0))

    # Add text score : next to the canvas
    text = font.render("Score : " + str(score), True, (255, 255, 255))
    window.blit(text, (500, 0))

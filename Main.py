import cv2
import mediapipe as mp
import numpy as np
from PIL import Image
from PIL import ImageFilter
#from pynput.keyboard import Listener, Key
import time



cap = cv2.VideoCapture(0)
pTime = 0
tmpcordX = -1
tmpcordY = -1
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
Erase = True
Position = False

canvasToSave = np.zeros((1080, 1920, 3), np.uint8)
canvasToSave[:] = 255, 255, 255

canvas = np.zeros((1080, 1920, 3), np.uint8)
cv2.imshow("Canvas", canvas)
cv2.imshow("Canvas", canvas)


    

def drawLine(a, b):
    global tmpcordX, tmpcordY
    if tmpcordX == -1 and tmpcordY == -1:
        tmpcordX = a
        tmpcordY = b

    if Erase == True:
        cv2.line(canvas, (tmpcordX, tmpcordY), (a, b), (255, 255, 255), 50)
        cv2.line(canvasToSave, (tmpcordX, tmpcordY), (a, b), (0, 0, 0), 50)
    else:
        cv2.line(canvas, (0, 0), (1, 1), (255, 255, 255), 15)
        print("Coords de 8", a, b)
        print("Coords de 7", tmpcordX, tmpcordY)
        cv2.line(canvas, (tmpcordX, tmpcordY), (a, b), (0, 0, 0), 50)
        cv2.line(canvasToSave, (tmpcordX, tmpcordY), (a, b), (255, 255, 255), 50)
    cv2.imshow("Canvas", canvas)
    tmpcordX = a
    tmpcordY = b
    cv2.imwrite("canvas.jpg", canvasToSave)
    #create an image from the area (300, 100), (1200, 1000) of the canvas and save it in the folder
    img = Image.open("canvas.jpg")
    img = img.crop((300, 100, 1200, 1000))
    img.save("canvas.jpg")

    



valFinger = 0

while True:    
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    cv2.rectangle(img, (300, 100), (1200, 1000), (0, 255, 0), 2)
    if results.multi_hand_landmarks and len(results.multi_hand_landmarks) == 2: 
        print ("2 mains détectées")
        #cv2.imshow("Canvas", canvas)
        #c
            #if results.multi_hand_landmarks and len(results.multi_hand_landmarks) > 1:
            #    start_time = time.time()
            #while (time.time() - start_time) < 1:
            #    success, img = cap.read()
            #    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            #    results = hands.process(imgRGB)
            #    cv2.imshow("Image", img)
            #    # check if one hand is removed during the countdown
            #    if len(results.multi_hand_landmarks) < 2:
            #        break
            #else:
            #    canvasToSave[:] = 255, 255, 255
            #    canvas[:] = 0, 0, 0
    if results.multi_hand_landmarks and len(results.multi_hand_landmarks) == 1: # Now detect only one hand
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
                if id == 8:
                    print("Coords de 8", cx, cy)
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                    tmpx8 = cx
                    tmpy8 = cy     
            if tmpx7 != 0 and tmpy7 != 0 and tmpx8 != 0 and tmpy8 != 0:
                if tmpy7 < tmpy8:
                    tmpcordX = -1
                    tmpcordY = -1
                    print("Doigt Baissé")
                else :
                    tmpx8 = 1920 - tmpx8
                    drawLine(tmpx8, tmpy8)
            if tmpx19 != 0 and tmpy19 != 0 and tmpx20 != 0 and tmpy20 != 0 and tmpx11 != 0 and tmpy11 != 0 and tmpx12 != 0 and tmpy12 != 0 and tmpx15 != 0 and tmpy15 != 0 and tmpx16 != 0 and tmpy16 != 0 and tmpx4 != 0 and tmpy4 != 0 and tmpx8 != 0 and tmpy8 != 0:
                if tmpy19 < tmpy20 and tmpy11 < tmpy12 and tmpy15 < tmpy16:
                    print("photo")
                    canvasToSave[:] = 255, 255, 255
                    canvas[:] = 0, 0, 0
                else :
                    if tmpy19 < tmpy20:
                        print("Doigt Baissé")
                        if(Position == True):
                            Position = False
                            if (Erase == False):
                                #Erase = True
                                null = 0
                            else :
                                null = 0
                                #Erase = False
                    else :
                        tmpx20 = 1920 - tmpx20
                        if(Position == False):
                            Position = True
                
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
    
    else : 
        tmpcordX = -1
        tmpcordY = -1
    img = cv2.flip(img, 1)
    cv2.imshow("Image", img)
    cv2.addWeighted(canvas, 1, img, 1, 1, img)
    cv2.imshow("Image", img)
    cv2.waitKey(1)



#pytorch
#sofrmax
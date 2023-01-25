import cv2
import mediapipe as mp
import numpy as np
cap = cv2.VideoCapture(0)
pTime = 0
#Define tmpcordX and tmpcordY
tmpcordX = -1
tmpcordY = -1
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
Erase = False
Position = False

canvas = np.zeros((1080, 1920, 3), np.uint8)
cv2.imshow("Canvas", canvas)
#Change canvas color to white
canvas[:] = 255, 255, 255

def drawLine(a, b):
    global tmpcordX, tmpcordY
    if tmpcordX == -1 and tmpcordY == -1:
        tmpcordX = a
        tmpcordY = b

    if Erase == True:
        #Draw a line between tmpcordX, tmpcordY and a, b
        cv2.line(canvas, (tmpcordX, tmpcordY), (a, b), (255, 255, 255), 15)
    else:
        cv2.line(canvas, (0, 0), (1, 1), (255, 255, 255), 15)
        print("Coords de 8", a, b)
        print("Coords de 7", tmpcordX, tmpcordY)
        #cv2.line(canvas, (tmpcordX, tmpcordY), (a, b), (255, 255, 255), 15)
        #cv2.circle(canvas, (a, b), 15, (255, 255, 255), -1)
        cv2.line(canvas, (tmpcordX, tmpcordY), (a, b), (0, 0, 0), 15)
    cv2.imshow("Canvas", canvas)
    tmpcordX = a
    tmpcordY = b

valFinger = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                if id == 19:
                    tmpx19 = cx
                    tmpy19 = cy
                if id == 20:
                    tmpx20 = cx
                    tmpy20 = cy
                if id == 7: 
                    tmpx7 = cx
                    tmpy7 = cy
                if id == 8:
                    print("Coords de 8", cx, cy)
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                    tmpx8 = cx
                    tmpy8 = cy     
            if tmpx7 != 0 and tmpy7 != 0 and tmpx8 != 0 and tmpy8 != 0:
                if tmpy7 < tmpy8:
                    print("Doigt Baissé")
                else :
                    tmpx8 = 1920 - tmpx8
                    drawLine(tmpx8, tmpy8)
            if tmpx19 != 0 and tmpy19 != 0 and tmpx20 != 0 and tmpy20 != 0:
                if tmpy19 < tmpy20:
                    print("Doigt Baissé")
                    if(Position == True):
                        Position = False
                        if (Erase == False):
                            Erase = True
                        else :
                            Erase = False

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
    cv2.waitKey(1)



pytorch
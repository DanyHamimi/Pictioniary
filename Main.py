import cv2
import mediapipe as mp
import numpy as np
cap = cv2.VideoCapture(0)
pTime = 0

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

canvas = np.zeros((1080, 1920, 3), np.uint8)
cv2.imshow("Canvas", canvas)

def drawLine(a, b):
    cv2.circle(canvas, (a, b), 15, (255, 255, 255), -1)
    cv2.imshow("Canvas", canvas)


while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
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
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
    img = cv2.flip(img, 1)
    cv2.imshow("Image", img)
    cv2.waitKey(1)




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
from utils import drawLine, imagePrediction

tmpcordX = -1
tmpcordY = -1

def recvall(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

def send_image(client_socket):
    while True:
        try:
            canvas_img = Image.fromarray(canvasToSave)
            canvas_img = canvas_img.crop((200, 50, 550, 400))
            canvas_img = canvas_img.resize((350, 350))
            img_byte_arr = io.BytesIO()
            canvas_img.save(img_byte_arr, format='JPEG')
            image_data = img_byte_arr.getvalue()


            size = len(image_data)
            score_bytes = struct.pack('>I', score)
            size_bytes = size.to_bytes(4, byteorder='big')
            client_socket.sendall(score_bytes)
            client_socket.sendall(size_bytes)
            client_socket.sendall(image_data)

            #print(f'Image sent with size {size/1024} ko')
        except Exception as e:
            print(e)
        time.sleep(0.01)


def win():
    window.fill((255, 255, 255))
    window.blit(background, (0, 0))
    font = pygame.font.SysFont('Arial', 100)
    text = font.render("Tu as gagné", True, (255, 255, 255))
    text_rect = text.get_rect(center=(1280 // 2, 720 // 2))
    window.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(3000)

def loose():
    window.fill((255, 255, 255))
    window.blit(background, (0, 0))
    font = pygame.font.SysFont('Arial', 100)
    text = font.render("Tu as perdu", True, (255, 255, 255))
    text_rect = text.get_rect(center=(1280 // 2, 720 // 2))
    window.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(3000)
    
def receive_and_process_images(client_socket):
    global ValToFindReally
    while True:
        try :
            int_data = client_socket.recv(4)
            if not int_data or len(int_data) < 4: break
            int_val = struct.unpack('>I', int_data)[0]
            print("On a recu" , int_val)
            if(int_val != 4294965296):
                score_data = client_socket.recv(4)
                if not score_data: continue
                score = struct.unpack('>I', score_data)[0]
                if(score==5):
                    loose()
                    break
                data = client_socket.recv(4)
                if not data: continue
                length = struct.unpack('>I', data)[0]
                img_data = b''
                while len(img_data) < length:
                    img_data += client_socket.recv(min(length - len(img_data), 4096))
                #print(f'Image received with size {length/1024} bytes and score {score}.')
                img = Image.open(io.BytesIO(img_data))
                canvasRecived = img.copy().convert('RGBA')
                canvasRecived = canvasRecived.resize((350, 350))
                window.blit(pygame.image.frombuffer(canvasRecived.tobytes(), canvasRecived.size, canvasRecived.mode), (900, 340))
                textVal = font.render("Score " + str(score), True, (0, 138, 138))
                window.blit(textVal, (920, 360))
            else : 
                print('on rentre ici')
                int_newValue = client_socket.recv(4)
                if not int_newValue: continue
                newValue = struct.unpack('>I', int_newValue)[0]
                print("newValue",newValue)
                window.blit(buttonVal2Find, (750, 50))
                textNb = font.render("Chiffre à trouver : " + str(newValue), True, (255, 255, 255))
                window.blit(textNb, (825, 65))
                ValToFindReally = newValue
                valFinded = -2


        except Exception as e:
            print(e)
            continue







def main(valToFind, servIndex):
    global valFinded
    global imageFrame
    global byteFrame
    global username
    global servIndexUser
    servIndexUser = servIndex
    username = ""
    global score
    score = 0
    isTesting = False
    SERVER_HOST = 'rayanekaabeche.fr'
    SERVER_PORT = 8080
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    servIndexUser_bytes = struct.pack('>I', servIndexUser)
    client_socket.sendall(servIndexUser_bytes)

    send_thread = threading.Thread(target=send_image, args=(client_socket,))
    receive_thread = threading.Thread(target=receive_and_process_images, args=(client_socket,))
    send_thread.start()
    receive_thread.start()

    while True:

        pygame.display.update()

        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

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
                            tmpcordX = -1  
                            tmpcordY = -1  
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
                            window.blit(buttonValFinded, (750, 150))
                            textVal = font.render("Chiffre trouvé : " + str(valFinded), True, (255, 255, 255))
                            print("Chiffre à trouver : " + str(ValToFindReally))
                            window.blit(textVal, (825, 165))
                            if ValToFindReally == valFinded:
                                
                                score += 1
                                #window.blit(buttonVal2Find, (750, 50))
                                #textNb = font.render("Chiffre à trouver : " + str(valToFind), True, (255, 255, 255))
                                #window.blit(textNb, (825, 65))
                                #valFinded = -2
                        except Exception as e:
                            print("error")
                            print(e)
                    else:
                        tmpx8 = 640 - tmpx8
                        isTesting = False

                        drawLine(tmpx8, tmpy8, tmpcordX, tmpcordY)
                        tmpcordX = tmpx8
                        tmpcordY = tmpy8

                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

        else:
            tmpcordX = -1
            tmpcordY = -1
        img = cv2.flip(img, 1)
        # cv2.imshow("Image", img)
        cv2.addWeighted(canvas, 1, img, 1, 1, img)
        # cv2.imshow("Image", img)
        cv2.waitKey(1)

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    
        frame = img_rgb
        frame = np.rot90(frame)


        frame = pygame.surfarray.make_surface(frame)
        frameCanvas = pygame.surfarray.make_surface(img_rgb)

        frameCanvas = pygame.transform.rotate(frameCanvas, 90)

        frameCanvas = pygame.transform.flip(frameCanvas, False, True)
        window.blit(frameCanvas, (0, 0))
        if score == 5:
            win()
            break
        text = font.render("Score : " + str(score), True, (255, 255, 255))
        window.blit(text, (500, 0))

        #Save canvas to image
        byteFrame = pygame.image.tostring(frameCanvas, 'RGBA')

    
        
        


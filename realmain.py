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
global score
score = 0


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

def loose():
    window.fill((255, 255, 255))
    window.blit(background, (0, 0))
    font = pygame.font.SysFont('Arial', 100)
    text = font.render("Tu as perdu", True, (255, 255, 255))
    text_rect = text.get_rect(center=(1280 // 2, 720 // 2))
    window.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(3000)

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



    
def receive_and_process_images(client_socket):
    global ValToFindReally
    global inGame
    while True:
        try :
            int_data = client_socket.recv(4)
            if not int_data or len(int_data) < 4: break
            int_val = struct.unpack('>I', int_data)[0]
            #print("On a recu" , int_val)
            if(int_val != 4294965296):
                score_data = client_socket.recv(4)
                if not score_data: continue
                score = struct.unpack('>I', score_data)[0]
                if(score==5):
                    loose()
                    inGame = False
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
                if(newValue == 14):
                    textNb = font.render("Attente", True, (255, 255, 255))
                    ValToFindReally = -1
                else :
                    textNb = font.render("Valeur à trouver : " + str(newValue), True, (255, 255, 255))
                    ValToFindReally = newValue
    
                window.blit(textNb, (825, 65))
                valFinded = -2


        except Exception as e:
            print(e)
            continue



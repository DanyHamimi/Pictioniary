import random
import struct
import numpy as np

import pygame
import regex

# Create a window using pygame
pygame.init()

window = pygame.display.set_mode((1280, 720))
score = 0


import time
import io
from PIL import Image
import socket
import struct
import threading

valToFind = "test"
# Create a canvas called canvasToSave
canvasToSave = np.zeros((640, 480, 3), np.uint8)
canvasToSave[:] = 100, 255, 255
font = pygame.font.SysFont("Arial", 30)
canvasRecived = np.zeros((640, 480, 3), np.uint8)


def recv_until(sock, delimiter):
    data = bytearray()
    while True:
        b = sock.recv(1)
        if not b or b == delimiter:
            break
        data.extend(b)
    return bytes(data)


def send_image(client_socket):
    while True:
        try:
            # Convert
            canvas_img = Image.fromarray(canvasToSave)
            canvas_img = canvas_img.crop((200, 50, 550, 400))
            canvas_img = canvas_img.resize((350, 350))
            img_byte_arr = io.BytesIO()
            canvas_img.save(img_byte_arr, format="JPEG")
            image_data = img_byte_arr.getvalue()

            size = len(image_data)
            score_bytes = struct.pack(">I", score)
            size_bytes = size.to_bytes(4, byteorder="big")
            client_socket.sendall(score_bytes)
            client_socket.sendall(size_bytes)
            client_socket.sendall(image_data)

            # print(f'Image sent with size {size/1024} ko')
        except Exception as e:
            print(e)
        time.sleep(0.1)


def receive_and_process_images(client_socket):
    global ValToFindReally
    global inGame
    while True:
        try:
            print("je suis ici")
            int_data = client_socket.recv(4)
            if not int_data or len(int_data) < 4:
                break
            int_val = struct.unpack(">I", int_data)[0]
            print("valeur recue" + str(int_val))
            if int_val != 500 and int_val != 450:
                score_data = client_socket.recv(4)
                if not score_data:
                    continue
                print("score recu" + str(score_data))
                score = struct.unpack(">I", score_data)[0]
                if score == 500:
                    print("PERDU")
                    inGame = False
                    break
                data = client_socket.recv(4)
                if not data:
                    continue
                length = struct.unpack(">I", data)[0]
                img_data = b""
                while len(img_data) < length:
                    img_data += client_socket.recv(min(length - len(img_data), 4096))
                # print(f'Image received with size {length/1024} bytes and score {score}.')
                img = Image.open(io.BytesIO(img_data))
                canvasRecived = img.copy().convert("RGBA")
                canvasRecived = canvasRecived.resize((350, 350))
                window.blit(canvasRecived, (850, 100))

                # Recive a string
                username_length_data = client_socket.recv(4)
                if not username_length_data:
                    continue
                username_length = struct.unpack(">I", username_length_data)[0]

                username_data = b""
                while len(username_data) < username_length:
                    username_data += client_socket.recv(
                        min(username_length - len(username_data), 4096)
                    )
                if not username_data:
                    continue
                username = username_data.decode()
                print("image recue")
            else:
                print("on rentre ici")
                value_length_data = client_socket.recv(4)
                if not value_length_data:
                    continue
                value_length = struct.unpack(">I", value_length_data)[0]

                newValue_data = b""
                while len(newValue_data) < value_length:
                    received_data = client_socket.recv(
                        min(value_length - len(newValue_data), 4096)
                    )
                    if not received_data:
                        break
                    newValue_data += received_data
                if not newValue_data:
                    continue
                newValue = newValue_data.decode()
                print("newValue", newValue)
                # window.blit(buttonVal2Find, (750, 50))
                # if(newValue == 14):
                # textNb = font.render("Attente", True, (255, 255, 255))
                # ValToFindReally = -1
                # else :
                # textNb = font.render("Valeur à trouver : " + str(newValue), True, (255, 255, 255))
                # ValToFindReally = newValue

                # window.blit(textNb, (825, 65))
                valFinded = -2

        except Exception as e:
            print(e)
            continue


# Boucle principale Pygame
if 1 == 1:
    SERVER_HOST = "localhost"
    SERVER_PORT = 8080
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        valueWelcome = "dany"
        client_socket.sendall((valueWelcome + "\n").encode())

        # Send int
        servIndexUser = 1
        servIndexUser_bytes = struct.pack(">I", servIndexUser)
        client_socket.sendall(servIndexUser_bytes)

        try:
            # Revice an int
            int_data = client_socket.recv(4)
            servIndex = struct.unpack(">I", int_data)[0]
            print(servIndex)
            if servIndex == 400:
                print("Erreur serveur plein")
                exit()

            value_length_data = client_socket.recv(4)
            value_length = struct.unpack(">I", value_length_data)[0]
            newValue_data = b""
            print("value_length", value_length)
            while len(newValue_data) < value_length:
                received_data = client_socket.recv(
                    min(value_length - len(newValue_data), 4096)
                )
                if not received_data:
                    break
                newValue_data += received_data
            newValue = newValue_data.decode()
            print("newValue", newValue)
            send_thread = threading.Thread(target=send_image, args=(client_socket,))
            receive_thread = threading.Thread(
                target=receive_and_process_images, args=(client_socket,)
            )
            send_thread.start()
            receive_thread.start()
        except socket.timeout:
            # Gérer l'erreur de timeout ici
            pass

    except ConnectionRefusedError:
        print("Connexion refusée par le serveur")
        # Gérer l'erreur de connexion refusée ici
        pass

while True:
    # Set canvas to save to a random color
    # canvasToSave[:] = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    # If key x pressed do something
    # Gérer les événements Pygame
    for event in pygame.event.get():
        # Si l'utilisateur clique sur la croix en haut à droite de la fenêtre, fermer l'application
        if event.type == pygame.QUIT:
            pygame.quit()

        # If key x pressed do something
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                print("x pressed")
                score = score + 1
    # Dessiner le canvas et les autres éléments de l'interface utilisateur
    window.fill((255, 255, 255))
    # Dessiner le canvas
    # Create a pygame surface from canvasToSave canvas
    canvasToSave [:] = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    canvasToSaveSurface = pygame.surfarray.make_surface(canvasToSave)
    canvasRecivedSurface = pygame.surfarray.make_surface(canvasRecived)

    window.blit(canvasToSaveSurface, (0, 0))
    window.blit(canvasRecivedSurface, (900, 340))
    # Afficher le score
    score_text = font.render("Score: " + str(score), True, (0, 0, 0))
    window.blit(score_text, (0, 0))

    # Rafraîchir l'affichage de la fenêtre
    pygame.display.update()

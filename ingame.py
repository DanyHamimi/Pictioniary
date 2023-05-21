import random
import string
import re
import sys
import os
import io
import socket
import struct
import time
import threading


from utils import *

has2Hands = False
global score
valToFind = "0"
scorePlayer2 = 0
scorePlayer3 = 0
scorePlayer4 = 0
AmountPlayer = 0
currentModel = None
current_letter_index = None
letters_found = None

ListPlayers = []

global send_thread
global receive_thread
fontMOT = pygame.font.Font('freesansbold.ttf', 60)
stop_flag = threading.Event()
isEndend = 0
Online = 0
typeGa = ""
back_text = font.render("Quitter", True, (255, 255, 255))
back_button_width = 150
back_button_height = 50
back_button_x = 50
back_button_y = 650
back_button = pygame.Rect(back_button_x, back_button_y,
                          back_button_width, back_button_height)


def setGameType(gameType):
    """
    Cette fonction prend en paramètre le type de jeu et retourne le modèle à utiliser.
    Argument:
        gameType (str): Le type de jeu ("Pictionary", "Mots" ou "Mathématiques").
    Return:
        object: Le modèle à utiliser en fonction du type de jeu.
    """
    if (gameType == "Pictionary"):
        return modelDraw
    elif (gameType == "Mots"):
        return modelLetters
    elif (gameType == "Mathématiques"):
        return model


def loose():
    """
    Cette fonction affiche un écran de défaite.
    """
    window.fill((255, 255, 255))
    window.blit(background, (0, 0))
    font = pygame.font.SysFont('Arial', 100)
    text = font.render("Tu as perdu", True, (255, 255, 255))
    text_rect = text.get_rect(center=(1280 // 2, 720 // 2))
    window.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(3000)


def predictImage(typeGame):
    """
    Cette fonction prend en paramètre le type de jeu et prédit le résultat de l'image.
    Arguments:
        typeGame (str): Le type de jeu ("Pictionary", "Mots" ou "Mathématiques").
    Return:
        str: La valeur prédite pour l'image par le modele.
    """
    valFinded = predict(preprocess_image(
        "Imgs/canvas.jpg", typeGame), currentModel, typeGame)
    window.blit(buttonValFinded, (750, 150))
    textVal = font.render(str(valFinded), True, (255, 255, 255))
    window.blit(textVal, (825, 165))
    return valFinded


def generateOtherValToFind(typeGame):
    """
    Cette fonction prend en paramètre le type de jeu et génère une nouvelle valeur à trouver.
    Argument:
        typeGame (str): Le type de jeu ("Pictionary", "Mots" ou "Mathématiques").
    Return:
        str: La nouvelle valeur à trouver générée selon le typeGame.
    """
    global Online
    if Online != "Solo":
        return valToFind
    if (typeGame == "Pictionary"):
        # Pick a random word from objet_name array
        return random.choice(objet_names)
    elif (typeGame == "Mots"):
        # Generate random letter
        with open("Mots.txt", "r") as file:
            words = file.readlines()
        word_to_find = random.choice(words).strip()
        # print("Mot à trouver : " + word_to_find)
        return word_to_find
    elif (typeGame == "Mathématiques"):
        result = random.randint(0, 9)

        operator = random.choice(["+", "-", "*", "//"])
        if operator == "+":
            num1 = random.randint(0, result)
            num2 = result - num1
        elif operator == "-":
            num1 = random.randint(result, 1000)
            num2 = num1 - result
        elif operator == "*":
            num1 = random.choice([i for i in range(1, 10) if result % i == 0])
            num2 = result // num1
        else:  # operator == "//"
            num1 = random.randint(1, 9)
            num2 = num1 * result
            while num2 == 0:  # Check for division by 0
                num1 = random.randint(1, 9)
                num2 = num1 * result
            return str(result) + ";" + str(num2) + operator + str(num1)
        return str(result) + ";" + str(num1) + operator + str(num2)


canvasPlayer2 = np.zeros((480, 640, 3), np.uint8)
canvasPlayer2[:] = 255, 255, 255
player2Surface = pygame.surfarray.make_surface(canvasPlayer2)


def display_current_word(word, letters_found):
    """
    Cette fonction prend en paramètres le mot en cours et les lettres déjà trouvées et retourne le mot affiché avec les lettres trouvées.
    Arguments:
        word (str): Le mot en cours.
        letters_found (set): Les lettres déjà trouvées.
    Return:
        str: Le mot affiché avec les lettres trouvées.
    """
    displayed_word = ""
    for letter in word:
        if letter in letters_found:
            displayed_word += letter
        else:
            displayed_word += " "
    return displayed_word


def updateNewOlineValue(newVal, typeGa):
    """
    Cette fonction prend en paramètres la nouvelle valeur en ligne et le type de jeu, et met à jour la variable valToFind
    lorsque celle ci a été envoyée par le serveur et que donc le joueur joue en ligne.
    Arguments:
        newVal (str): La nouvelle valeur en ligne.
        typeGa (str): Le type de jeu ("Pictionary", "Mots" ou "Mathématiques").
    """
    global current_letter_index
    global letters_found
    global valToFind
    if typeGa == "Mathématiques":
        # print("Math")
        valToFindTMP = newVal
        # print(valToFindTMP)
        valToFind = valToFindTMP.split(";")[0]
        calculus = valToFindTMP.split(";")[1]
        setNewValue(typeGa, calculus)
    else:
        if typeGa == "Mots":
            init(typeGa)
        current_letter_index = 0
        letters_found.clear()
        valToFind = newVal
        setNewValue(typeGa, valToFind)
    canvasToSave[:] = 255, 255, 255
    canvas[:] = 0, 0, 0


def send_image(client_socket):
    """
    Cette fonction prend en paramètre le socket du client et envoie l'image contenue dans le canvas du client au serveur
    pour ensuite l'envoyer aux autres joueurs et s'execute en boucle tant que le client ne quitte pas la partie ou qu'un joueur 
    ne gagne pas.
    Argument:
        client_socket (socket): Le socket du client.
    """
    global stop_flag
    global isEndend
    while not stop_flag.is_set():
        try:
            # print("envoie")
            # Convert
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

        except Exception:
            isEndend = 1
            sys.exit()
            break
        time.sleep(0.1)


def drawPlayerXcanvas(canvasRecived, id, scorep, usernamep):
    """
    Cette fonction prend en paramètres le canvas reçu du serveur, l'identifiant du joueur, son score et son nom d'utilisateur,
    et dessine le canvas du joueur X à l'écran.
    Arguments:
        canvasRecived (np.ndarray): Le canvas reçu du serveur.
        id (int): L'identifiant du joueur afin de pouvoir savoir ou placer le dessin.
        scorep (int): Le score du joueur.
        usernamep (str): Le nom d'utilisateur du joueur.
    """
    global AmountPlayer
    global ListPlayers
    # Convert AmontPlayer to int
    userNameWithoutSpace = usernamep.replace("\0", "")
    if int(AmountPlayer) > 2:
        canvasRecived = canvasRecived.resize((233, 240))
        fontUser_Score = pygame.font.SysFont('freesansbold', 25)
        try:
            print("ici")
            # Selon la postion de id dans le tableau on blit le canvas à un endroit différent
            if id == ListPlayers[0]:
                window.blit(pygame.image.frombuffer(canvasRecived.tobytes(
                ), canvasRecived.size, canvasRecived.mode), (698, 480))
                text = fontUser_Score.render(
                    userNameWithoutSpace+" :", True, (0, 0, 0))
                window.blit(text, (698, 480))
                text = fontUser_Score.render(
                    "Score : "+str(scorep), True, (0, 0, 0))
                window.blit(text, (698, 500))
                return
            elif id == ListPlayers[1]:
                window.blit(pygame.image.frombuffer(canvasRecived.tobytes(
                ), canvasRecived.size, canvasRecived.mode), (698+234, 480))
                text = fontUser_Score.render(
                    userNameWithoutSpace+" :", True, (0, 0, 0))
                window.blit(text, (698+234, 480))
                text = fontUser_Score.render(
                    "Score : "+str(scorep), True, (0, 0, 0))
                window.blit(text, (698+234, 500))

                return
            elif id == ListPlayers[2]:
                window.blit(pygame.image.frombuffer(canvasRecived.tobytes(
                ), canvasRecived.size, canvasRecived.mode), (814, 240))
                text = fontUser_Score.render(
                    userNameWithoutSpace+" :", True, (0, 0, 0))
                window.blit(text, (814, 240))
                text = fontUser_Score.render(
                    "Score : "+str(scorep), True, (0, 0, 0))
                window.blit(text, (814, 260))
                return
        except Exception as e:
            print(e)
            return
    else:
        window.blit(pygame.image.frombuffer(canvasRecived.tobytes(),
                    canvasRecived.size, canvasRecived.mode), (900, 340))
        # Write into the canvas the score and the username
        text = font.render(userNameWithoutSpace+" :", True, (255, 255, 255))
        window.blit(text, (900, 300))
        text = font.render("Score : "+str(scorep), True, (0, 0, 0))
        window.blit(text, (900, 350))

        return


def receive_and_process_images(client_socket):
    """
    Cette fonction prend en paramètre le socket du client et reçoit et traite les images envoyées par le serveur en les placant au bon endroit
    et s'execute en boucle tant que le client ne quitte pas la partie ou qu'un joueur 
    ne gagne pas.
    Args:
        client_socket (socket): Le socket du client.
    """
    global typeGa
    global valToFind
    global inGame
    global scorePlayer2
    global stop_flag
    global isEndend
    global ListPlayers
    while not stop_flag.is_set():
        # print("recoit")
        try:
            int_data = client_socket.recv(4)
            if not int_data or len(int_data) < 4:
                break
            int_val = struct.unpack(">I", int_data)[0]
            if int_val != 500 and int_val != 450:
                score_data = client_socket.recv(4)
                if not score_data:
                    continue
                score = struct.unpack(">I", score_data)[0]
                print("score recu" + str(score))
                id_recived = client_socket.recv(4)
                if not id_recived:
                    continue
                id = struct.unpack(">I", id_recived)[0]
                print("id recu" + str(id))
                # si l'id recu n'est pas dans le tableau des players alors on l'ajoute
                if id not in ListPlayers:
                    ListPlayers.append(id)
                data = client_socket.recv(4)
                if not data:
                    continue
                length = struct.unpack(">I", data)[0]
                img_data = b""
                while len(img_data) < length:
                    img_data += client_socket.recv(
                        min(length - len(img_data), 4096))
                # print(f'Image received with size {length/1024} bytes and score {score}.')
                img = Image.open(io.BytesIO(img_data))
                canvasRecived = img.copy().convert("RGBA")
                canvasRecived = canvasRecived.resize((350, 350))
                # window.blit(pygame.image.frombuffer(canvasRecived.tobytes(), canvasRecived.size, canvasRecived.mode), (900, 340))

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
                usernameR = username_data.decode()
                print("usernameR", usernameR)
                drawPlayerXcanvas(canvasRecived, id, score, usernameR)
            else:
                value_length_data = client_socket.recv(4)
                if not value_length_data:
                    continue
                value_length = struct.unpack(">I", value_length_data)[0]

                newValue_data = b""
                # print("value_length", value_length)
                while len(newValue_data) < value_length:
                    received_data = client_socket.recv(
                        min(value_length - len(newValue_data), 4096))
                    if not received_data:
                        break
                    newValue_data += received_data
                newValue = newValue_data.decode()
                valToFind = newValue.upper()
                # print("newValue", newValue)
                updateNewOlineValue(newValue.upper(), typeGa)

        except Exception as e:
            print(e)
            print("DECONNECTE")

            break


def mainGame(isonline, gameType, idServ, ipServ, nbPlayers, username):
    # print("Partie avec "+nbPlayers+" joueurs")
    global score
    global valToFind
    global stop_flag
    global isEndend
    global Online
    global typeGa
    global has2Hands
    global AmountPlayer
    global currentModel
    global current_letter_index
    global letters_found

    typeGa = gameType
    Online = isonline

    AmountPlayer = nbPlayers

    score = 0
    valToFind = generateOtherValToFind(gameType)
    if (isonline != "Solo"):

        SERVER_HOST = ipServ
        SERVER_PORT = 8080
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((SERVER_HOST, SERVER_PORT))
            valueWelcome = username+";"+str(idServ)
            client_socket.sendall((valueWelcome + "\n").encode())

            try:
                # Revice an int
                int_data = client_socket.recv(4)
                servIndex = struct.unpack('>I', int_data)[0]
                # print(servIndex)
                if (servIndex == 400):
                    print("Impossible de rejoindre le serveur")
                    return

                value_length_data = client_socket.recv(4)
                value_length = struct.unpack('>I', value_length_data)[0]
                newValue_data = b''
                while len(newValue_data) < value_length:
                    received_data = client_socket.recv(
                        min(value_length - len(newValue_data), 4096))
                    if not received_data:
                        break
                    newValue_data += received_data
                newValue = newValue_data.decode()
                valToFind = newValue.upper()
                send_thread = threading.Thread(
                    target=send_image, args=(client_socket,))
                receive_thread = threading.Thread(
                    target=receive_and_process_images, args=(client_socket,))
                send_thread.start()
                receive_thread.start()
            except socket.timeout:
                pass

        except ConnectionRefusedError:
            print("Connexion refusée par le serveur")
            pass

    letters_found = set()
    current_letter_index = 0

    init(gameType)
    if (gameType == "Mathématiques"):
        setNewValue(gameType, valToFind.split(";")[1])
        valToFind = valToFind.split(";")[0]
    else:
        setNewValue(gameType, valToFind)

    currentModel = setGameType(gameType)
    gomme = True
    tmpcordX = -1
    tmpcordY = -1
    # servIndexUser = servIndex

    # print("Valeur a trouver : " + str(valToFind))
    if (isonline == "Solo"):
        start_time = time.time()
        clock = pygame.time.Clock()
    while True:

        if isonline == "Online":
            if isEndend == 1:
                isEndend = 0
                # print("Player 2 win")
                stop_flag.set()
                send_thread.join()
                receive_thread.join()
                client_socket.close()
                print("ciao")
                stop_flag.clear()
                ListPlayers.clear()
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            # print("photo")
            try:
                valFinded = predictImage(gameType)
                print("Valeur à trouver " + str(valToFind) +
                      "Valeur trouvée " + str(valFinded))
                if gameType == "Mots":
                    if valToFind[current_letter_index] == valFinded:
                        # print("Lettre trouvée dans l'ordre !")
                        lettertodraw = fontMOT.render(
                            str(valFinded), True, (0, 255, 0))
                        window.blit(
                            lettertodraw, (30+(current_letter_index*40), 485))
                        letters_found.add(valFinded)
                        current_letter_index += 1
                        if current_letter_index == len(valToFind):
                            # print("Toutes les lettres du mot ont été trouvées dans l'ordre !")
                            current_letter_index = 0
                            letters_found.clear()
                            score += 1
                            init(gameType)
                            if (isonline == "Solo"):
                                valToFind = generateOtherValToFind(gameType)
                            setNewValue(gameType, valToFind)
                if str(valToFind) == str(valFinded):
                    # print("trouvé")
                    score += 1
                    if (gameType == "Mathématiques" and isonline == "Solo"):
                        # print("Math")
                        valToFindTMP = generateOtherValToFind(gameType)
                        # print(valToFindTMP)
                        valToFind = valToFindTMP.split(";")[0]
                        calculus = valToFindTMP.split(";")[1]
                        setNewValue(gameType, calculus)
                    elif (isonline == "Solo"):
                        valToFind = generateOtherValToFind(gameType)
                        setNewValue(gameType, valToFind)
                    canvasToSave[:] = 255, 255, 255
                    canvas[:] = 0, 0, 0

            except Exception as e:
                print("error")
                print(e)

        pygame.display.update()
        if keys[pygame.K_w]:
            canvasToSave[:] = 255, 255, 255
            canvas[:] = 0, 0, 0

        if keys[pygame.K_x]:
            gomme = not gomme

        # print(valToFind)
        pygame.display.update()

        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        cv2.rectangle(img, (100, 50), (450, 400), (0, 255, 0), 2)
        if results.multi_hand_landmarks and len(results.multi_hand_landmarks) == 2 and has2Hands == False:
            has2Hands = True
            if has2Hands:
                print("2 mains détectées")

        # Now detect only one hand
        if results.multi_hand_landmarks and len(results.multi_hand_landmarks) == 1:
            has2Hands = False
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    if id == 8:
                        # print("Coords de 8", cx, cy)
                        cv2.circle(img, (cx, cy), 15,
                                   (255, 0, 255), cv2.FILLED)
                        tmpx8 = cx
                        tmpy8 = cy
                        if tmpx8 != 0 and tmpy8 != 0:
                            tmpx8 = 640 - tmpx8

                            drawLine(tmpx8, tmpy8, tmpcordX, tmpcordY, gomme)
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
                if isonline != "Solo":
                    stop_flag.set()
                    send_thread.join()
                    receive_thread.join()
                    client_socket.close()

                    break
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_button.collidepoint(mouse_pos):
                    if (isonline != "Solo"):
                        client_socket.close()
                        stop_flag.set()
                        send_thread.join()
                        receive_thread.join()
                        stop_flag.clear()
                        ListPlayers.clear()
                        return
                    window.fill((0, 0, 0))
                    pygame.display.update()
                    return
        if (isonline == "Solo"):
            elapsed_time = time.time() - start_time
            remaining_time = max(0, 90 - elapsed_time)
            minutes = int(remaining_time / 60)
            seconds = int(remaining_time % 60)
            timer_text = f"{minutes:02d}:{seconds:02d}"
            timer_surface = font.render(timer_text, True, (255, 255, 255))
            window.blit(butTimer, (1280 - 200, 720 - 100))
            window.blit(timer_surface, (1280 - 150, 720 - 75))
            if remaining_time <= 0:
                win(str(score))
                break
            clock.tick(60)

        frame = img_rgb
        frame = np.rot90(frame)

        frame = pygame.surfarray.make_surface(frame)
        frameCanvas = pygame.surfarray.make_surface(img_rgb)

        frameCanvas = pygame.transform.rotate(frameCanvas, 90)

        frameCanvas = pygame.transform.flip(frameCanvas, False, True)
        window.blit(frameCanvas, (0, 0))

        text = font.render("Score : " + str(score), True, (255, 255, 255))
        window.blit(text, (480, 0))

        # Save canvas to image
        byteFrame = pygame.image.tostring(frameCanvas, 'RGBA')

        # draw precedent button
        window.blit(back_text, (back_button.x + (back_button.width - back_text.get_width()) //
                    2, back_button.y + (back_button.height - back_text.get_height()) // 2))

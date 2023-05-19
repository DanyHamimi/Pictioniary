import string
import struct
import pygame
import math
import socket
from Main import main
from config import *
from utils import *
from solo import mainSolo

username = "user"

pygame.init()

server_button_width = 200
server_button_height = 80
server_button_start_y = 200
server_button_spacing = 100
server_button_join_width = 150
server_button_join_height = 50
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def show_servers_prerequest(ip, stringToSend):
    print("L'adresse IP saisie est :", ip)
    SERVER_HOST = ip
    SERVER_PORT = 8080
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(4)
    try:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        valueWelcome = stringToSend
        client_socket.sendall((valueWelcome + "\n").encode())
        try:
            welcomeMessage = client_socket.recv(1024)
            welcomemsg = welcomeMessage.decode()
            print(welcomemsg)
            show_servers(window, welcomemsg, ip)
        except socket.timeout:
            print("Timeout: No response received in 4 seconds. Disconnecting...")
        # Wait for server to send welcome message
        welcomeMessage = client_socket.recv(1024)
        print(welcomeMessage.decode())
        # Disconnect from server
        client_socket.close()
    except Exception as e:
        print(e)
        print("Impossible de se connecter au serveur. Retour au menu principal.")


def ask_for_ip(window):
    font = pygame.font.SysFont("Arial", 30)
    input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100,
                            SCREEN_HEIGHT // 2 - 20, 200, 40)
    text = ''
    active = False
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        window.fill((0, 0, 0))

        window.blit(background, (0, 0))

        txt_surface = font.render(text, True, (255, 255, 255))
        window.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(window, (255, 255, 255), input_box, 2)

        prompt = font.render(
            "Veuillez entrer une adresse IP :", True, (255, 255, 255))
        window.blit(prompt, (SCREEN_WIDTH // 2 -
                    prompt.get_width() // 2, SCREEN_HEIGHT // 2 - 80))

        pygame.display.update()

    return text


def show_game_modes(window):
    font = pygame.font.SysFont("Arial", 30)

    game_mode_buttons = []

    game_modes = ["Pictionary", "Mots", "Mathématiques"]
    button_start_y = 300
    button_spacing = 100

    for i, mode in enumerate(game_modes):
        button_y = button_start_y + i * button_spacing

        text = font.render(mode, True, (255, 255, 255))
        button = pygame.Rect(button_x, button_y, button_width, button_height)

        game_mode_buttons.append((button, text))

    # Ajouter un bouton "précédent"
    back_text = font.render("Précédent", True, (255, 255, 255))
    back_button_width = 150
    back_button_height = 50
    back_button_x = 50
    back_button_y = 50
    back_button = pygame.Rect(
        back_button_x, back_button_y, back_button_width, back_button_height)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if back_button.collidepoint(mouse_pos):
                    print("Le bouton Précédent a été cliqué !")
                    window.fill((0, 0, 0))
                    pygame.display.update()
                    return

                for i, (button, _) in enumerate(game_mode_buttons):
                    if button.collidepoint(mouse_pos):
                        print(
                            f"Le mode de jeu {game_modes[i]} a été sélectionné !")
                        window.fill((0, 0, 0))
                        pygame.display.update()
                        mainSolo("Solo", game_modes[i], -1, 0, 1, "user")

        window.blit(background, (0, 0))

        pygame.draw.rect(window, (255, 255, 255), back_button, 3)
        window.blit(back_text, (back_button.x + (back_button.width - back_text.get_width()) //
                    2, back_button.y + (back_button.height - back_text.get_height()) // 2))

        for button, text in game_mode_buttons:
            pygame.draw.rect(window, (255, 255, 255), button, 3)
            window.blit(text, (button.x + (button.width - text.get_width()) //
                        2, button.y + (button.height - text.get_height()) // 2))

        pygame.display.update()


background = pygame.image.load("Imgs/testfond.png")

logo = pygame.image.load("Imgs/testlogo.png")

buttonBis = pygame.image.load("Imgs/testbutton.png")
buttonQuitBis = pygame.image.load("Imgs/button2.png")
buttonSoloBis = pygame.image.load("Imgs/boutton_solo.png")

button = pygame.transform.scale(buttonBis, (200, 80))
buttonQuit = pygame.transform.scale(buttonQuitBis, (200, 80))
buttonSolo = pygame.transform.scale(buttonSoloBis, (200, 80))

logo_width = 1036
logo_height = 216
logo_x = (SCREEN_WIDTH - logo_width) // 2
logo_y = 70

font = pygame.font.SysFont("Arial", 50)

text = font.render("Play", True, (255, 255, 255))

button_width = 200
button_height = 80
button_x = (SCREEN_WIDTH - button_width) // 2
button_y = logo_y + logo_height + 100

textSolo = font.render("Solo", True, (255, 255, 255))

buttonSolo_width = 200
buttonSolo_height = 80
buttonSolo_x = (SCREEN_WIDTH - buttonSolo_width) // 2
buttonSolo_y = logo_y + logo_height + 200


buttonQuit_width = 200
buttonQuit_height = 80
buttonQuit_x = (SCREEN_WIDTH - buttonQuit_width) // 2
buttonQuit_y = logo_y + logo_height + 300


def show_servers(window, welcomemsg, ipserv):
    global username
    font = pygame.font.SysFont("Arial", 30)

    # Titre "LISTE DES PARTIES"
    # Police en gras avec une taille de 40
    title_font = pygame.font.SysFont("Arial", 40, True)
    title_text = title_font.render("LISTE DES PARTIES", True, (255, 255, 255))
    title_x = (window.get_width() - title_text.get_width()) // 2
    title_y = 50

    # Champ pour le nom d'utilisateur
    username_label = font.render("Pseudo: ", True, (255, 255, 255))
    username_text = username
    username_input_rect = pygame.Rect(150, window.get_height() - 100, 200, 50)
    username_input_active = False

    server_buttons = []
    join_buttons = []
    tableauMsgs = welcomemsg.split(";")
    tableauMsgs.pop()
    row = 0
    for index, msg in enumerate(tableauMsgs):
        server_button_y = server_button_start_y + \
            (index % 4) * server_button_spacing
        if index % 4 == 0:
            row += 1
        button_x = 150 + (row - 1) * (server_button_width + 350)
        nameServer = msg.split(" ")[0]
        amountPlayers = msg.split(" ")[2]
        typeGame = msg.split(" ")[3]
        server_button = pygame.Rect(
            button_x, server_button_y, server_button_width, server_button_height)

        server_text = font.render(nameServer, True, (255, 255, 255))
        join_text = font.render(amountPlayers, True, (255, 255, 255))
        join_button = pygame.Rect(button_x + server_button_width + 50, server_button_y + (
            server_button_height - server_button_join_height) // 2, server_button_join_width, server_button_join_height)

        server_buttons.append((server_button, server_text))
        join_buttons.append((join_button, join_text))

    back_text = font.render("Précédent", True, (255, 255, 255))
    back_button_width = 150
    back_button_height = 50
    back_button_x = 50
    back_button_y = 50
    back_button = pygame.Rect(
        back_button_x, back_button_y, back_button_width, back_button_height)

    reload_text = font.render("Recharger", True, (255, 255, 255))
    reload_button_width = 160
    reload_button_height = 50
    reload_button_x = 1100
    reload_button_y = 50
    reload_button = pygame.Rect(
        reload_button_x, reload_button_y, reload_button_width, reload_button_height)

    create_server_text = font.render("Créer une partie", True, (255, 255, 255))
    create_server_button_width = 240
    create_server_button_height = 80
    create_server_button_x = 1030
    create_server_button_y = 625

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if back_button.collidepoint(mouse_pos):
                    print("Le bouton Précédent a été cliqué !")
                    window.fill((0, 0, 0))
                    pygame.display.update()
                    return

                if reload_button.collidepoint(mouse_pos):
                    print("Le bouton Reload a été cliqué !")
                    window.fill((0, 0, 0))
                    pygame.display.update()
                    show_servers_prerequest(ip, "askserverforplayers")
                    return

                if create_server_button.collidepoint(mouse_pos):
                    print("Le bouton Create Server a été cliqué !")
                    window.fill((0, 0, 0))
                    pygame.display.update()
                    create_server(window)
                    return

                for i, (join_button, _) in enumerate(join_buttons):
                    if join_button.collidepoint(mouse_pos):
                        print(
                            f"Le bouton Rejoindre du serveur {i + 1} a été cliqué !")
                        window.fill((0, 0, 0))
                        pygame.display.update()
                        typeGame = tableauMsgs[i].split(" ")[3].capitalize()
                        if typeGame == "Mathematiques":
                            typeGame = "Mathématiques"
                        max_players = (tableauMsgs[i].split(" ")[
                                       2]).split("/")[1]
                        if (username == ""):
                            username = "user"
                        mainSolo("Online", typeGame, i,
                                 ipserv, max_players, username)
                        show_servers_prerequest(ip, "askserverforplayers")
                        return

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    # Action à effectuer lorsque la touche "Retour arrière" est enfoncée
                    username = username[:-1]
                    username_text = username
                else:
                    username += event.unicode

                    username_text = username

        window.blit(background, (0, 0))

        # Affichage du titre en gras
        window.blit(title_text, (title_x, title_y))

        # Affichage du champ d'entrée du nom d'utilisateur
        pygame.draw.rect(window, (255, 255, 255), username_input_rect, 3)
        window.blit(username_label, (username_input_rect.x -
                    120, username_input_rect.y + 10))
        username_input_text = font.render(username_text, True, (255, 255, 255))
        window.blit(username_input_text, (username_input_rect.x +
                    10, username_input_rect.y + 10))

        pygame.draw.rect(window, (255, 255, 255), back_button, 3)
        window.blit(back_text, (back_button.x + (back_button.width - back_text.get_width()) //
                    2, back_button.y + (back_button.height - back_text.get_height()) // 2))

        create_server_button = pygame.Rect(
            create_server_button_x, create_server_button_y, create_server_button_width, create_server_button_height)
        pygame.draw.rect(window, (255, 255, 255), create_server_button, 3)
        window.blit(create_server_text, (create_server_button.x + (create_server_button.width - create_server_text.get_width()
                                                                   ) // 2, create_server_button.y + (create_server_button.height - create_server_text.get_height()) // 2))

        pygame.draw.rect(window, (255, 255, 255), reload_button, 3)
        window.blit(reload_text, (reload_button.x + (reload_button.width - reload_text.get_width()) //
                    2, reload_button.y + (reload_button.height - reload_text.get_height()) // 2))

        for server_button, server_text in server_buttons:
            pygame.draw.rect(window, (255, 255, 255), server_button, 3)
            window.blit(server_text, (server_button.x + (server_button.width - server_text.get_width()) //
                        2, server_button.y + (server_button.height - server_text.get_height()) // 2))

        for join_button, join_text in join_buttons:
            pygame.draw.rect(window, (255, 255, 255), join_button, 3)
            window.blit(join_text, (join_button.x + (join_button.width - join_text.get_width()) //
                        2, join_button.y + (join_button.height - join_text.get_height()) // 2))

        pygame.display.update()


def create_server(window):
    font = pygame.font.SysFont("Arial", 30)
    input_boxes = []
    labels = []
    fields = ["Nom de la partie"]

    label_width = 200
    label_height = 40
    label_x = SCREEN_WIDTH // 2 - label_width - 50

    input_box_width = 200
    input_box_height = 40
    input_box_x = SCREEN_WIDTH // 2 + 50

    button_width = 200
    button_height = 80
    button_x = SCREEN_WIDTH // 2 - button_width // 2

    inputs = [""]

    for i, field in enumerate(fields):
        label = font.render(field + " :", True, (255, 255, 255))
        label_rect = label.get_rect(
            x=label_x, y=220 + i * 100, width=label_width, height=label_height)
        labels.append((label, label_rect))

        input_box = pygame.Rect(input_box_x, 220 + i *
                                100, input_box_width, input_box_height)
        input_boxes.append(input_box)

    confirm_text = font.render("Confirmer", True, (255, 255, 255))
    confirm_button = pygame.Rect(button_x, 500, button_width, button_height)

    cancel_text = font.render("Annuler", True, (255, 255, 255))
    cancel_button = pygame.Rect(button_x, 600, button_width, button_height)

    radio_buttons = []
    radio_labels = ["2 joueurs", "3 joueurs", "4 joueurs"]
    radio_button_width = 200
    radio_button_height = 50
    radio_button_spacing = 20
    radio_button_x = SCREEN_WIDTH // 2 - radio_button_width // 2 + 200

    for i, label in enumerate(radio_labels):
        radio_button_y = 300 + i * (radio_button_height + radio_button_spacing)
        radio_button = pygame.Rect(
            radio_button_x, radio_button_y, radio_button_width, radio_button_height)
        radio_buttons.append((radio_button, label))

    mode_buttons = []
    mode_labels = ["Pictionary", "Mots", "Mathematiques"]
    mode_button_width = 200
    mode_button_height = 50
    mode_button_spacing = 20
    mode_button_x = SCREEN_WIDTH // 2 - mode_button_width // 2 - 200

    for i, label in enumerate(mode_labels):
        mode_button_y = 300 + i * (mode_button_height + mode_button_spacing)
        mode_button = pygame.Rect(
            mode_button_x, mode_button_y, mode_button_width, mode_button_height)
        mode_buttons.append((mode_button, label))

    selected_player_count = 2
    selected_mode = "Pictionary"

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if confirm_button.collidepoint(mouse_pos):
                    if all(inputs):

                        game_type = selected_mode.lower()
                        game_name = inputs[0]
                        slots = str(selected_player_count)
                        request_string = f"createserver;{game_type};{game_name};{slots}"

                        show_servers_prerequest(ip, request_string)
                        return

                elif cancel_button.collidepoint(mouse_pos):
                    print("Le bouton Annuler a été cliqué !")
                    window.fill((0, 0, 0))
                    pygame.display.update()
                    return  # retourner à la fonction précédente

                for radio_button, label in radio_buttons:
                    if radio_button.collidepoint(mouse_pos):
                        selected_player_count = int(label.split()[0])

                for mode_button, label in mode_buttons:
                    if mode_button.collidepoint(mouse_pos):
                        selected_mode = label

            elif event.type == pygame.KEYDOWN:
                for i, input_box in enumerate(input_boxes):
                    if input_box.collidepoint(pygame.mouse.get_pos()):
                        active = True
                    else:
                        active = False
                    if active:
                        print("active")
                        if event.key == pygame.K_RETURN:
                            inputs[i] = input_text
                            input_text = ""
                        elif event.key == pygame.K_BACKSPACE:
                            input_text = input_text[:-1]
                            inputs[i] = input_text
                        else:
                            if (len(input_text) < 10):
                                if (event.unicode in string.ascii_letters or event.unicode in string.digits):
                                    input_text += event.unicode
                                    inputs[i] = input_text

        window.fill((0, 0, 0))
        window.blit(background, (0, 0))

        for label, label_rect in labels:
            window.blit(label, label_rect)

        for i, input_box in enumerate(input_boxes):
            pygame.draw.rect(window, (255, 255, 255), input_box, 2)
            input_text = inputs[i]
            input_surface = font.render(input_text, True, (255, 255, 255))
            window.blit(input_surface, (input_box.x + 5, input_box.y + 5))

        pygame.draw.rect(window, (255, 255, 255), confirm_button, 3)
        window.blit(confirm_text, (confirm_button.x + (confirm_button.width - confirm_text.get_width()) //
                    2, confirm_button.y + (confirm_button.height - confirm_text.get_height()) // 2))

        pygame.draw.rect(window, (255, 255, 255), cancel_button, 3)
        window.blit(cancel_text, (cancel_button.x + (cancel_button.width - cancel_text.get_width()) //
                    2, cancel_button.y + (cancel_button.height - cancel_text.get_height()) // 2))

        for radio_button, label in radio_buttons:
            if int(label.split()[0]) == selected_player_count:
                pygame.draw.rect(window, (255, 255, 255), radio_button, 3)
            else:
                pygame.draw.rect(window, (150, 150, 150), radio_button, 3)
            radio_text = font.render(label, True, (255, 255, 255))
            radio_text_rect = radio_text.get_rect(center=(
                radio_button.x + radio_button.width // 2, radio_button.y + radio_button.height // 2))
            window.blit(radio_text, radio_text_rect)

        for mode_button, label in mode_buttons:
            if label == selected_mode:
                pygame.draw.rect(window, (255, 255, 255), mode_button, 3)
            else:
                pygame.draw.rect(window, (150, 150, 150), mode_button, 3)
            mode_text = font.render(label, True, (255, 255, 255))
            mode_text_rect = mode_text.get_rect(center=(
                mode_button.x + mode_button.width // 2, mode_button.y + mode_button.height // 2))
            window.blit(mode_text, mode_text_rect)

        pygame.display.update()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height:
                print("Le bouton Play a été cliqué !")
                window.fill((0, 0, 0))
                pygame.display.update()
                ip = ask_for_ip(window)
                show_servers_prerequest(ip, "askserverforplayers")

            elif buttonQuit_x <= mouse_pos[0] <= buttonQuit_x + buttonQuit_width and buttonQuit_y <= mouse_pos[1] <= buttonQuit_y + buttonQuit_height:
                print("Le bouton Quit a été cliqué !")
                pygame.quit()
                quit()
            elif buttonSolo_x <= mouse_pos[0] <= buttonSolo_x + buttonSolo_width and buttonSolo_y <= mouse_pos[1] <= buttonSolo_y + buttonSolo_height:
                print("Le bouton Solo a été cliqué !")
                window.fill((0, 0, 0))
                pygame.display.update()
                show_game_modes(window)

    time = pygame.time.get_ticks() / 1000.0
    logo_y_offset = math.sin(time * 3) * 20

    window.blit(background, (0, 0))

    window.blit(logo, (logo_x, logo_y + logo_y_offset))

    window.blit(button, (button_x, button_y))

    window.blit(buttonSolo, (buttonSolo_x, buttonSolo_y))

    window.blit(buttonQuit, (buttonQuit_x, buttonQuit_y))

    pygame.display.update()

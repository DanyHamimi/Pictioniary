import struct
import pygame
import math
import socket
from Main import main
from config import *
from utils import *
from solo import mainSolo


pygame.init()

# Définir les dimensions de l'écran
server_button_width = 200
server_button_height = 80
server_button_start_y = 200
server_button_spacing = 100
server_button_join_width = 150
server_button_join_height = 50
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
def ask_for_ip(window):
    font = pygame.font.SysFont("Arial", 30)
    input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20, 200, 40)
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

        prompt = font.render("Veuillez entrer une adresse IP :", True, (255, 255, 255))
        window.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, SCREEN_HEIGHT // 2 - 80))

        pygame.display.update()

    return text
def connect_to_server(ip, port=12345):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((ip, port))
        return True
    except Exception as e:
        print(f"Erreur lors de la connexion au serveur: {e}")
        return False
    
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
    back_button = pygame.Rect(back_button_x, back_button_y, back_button_width, back_button_height)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Vérifier si le bouton "Précédent" est cliqué
                if back_button.collidepoint(mouse_pos):
                    print("Le bouton Précédent a été cliqué !")
                    window.fill((0, 0, 0))
                    pygame.display.update()
                    return  # retourner à la fonction précédente

                for i, (button, _) in enumerate(game_mode_buttons):
                    if button.collidepoint(mouse_pos):
                        print(f"Le mode de jeu {game_modes[i]} a été sélectionné !")
                        window.fill((0, 0, 0))
                        pygame.display.update()
                        # Remplacez cette ligne par le code pour lancer le mode de jeu sélectionné
                        mainSolo("Solo",game_modes[i])

        window.blit(background, (0, 0))

        # Afficher le bouton "Précédent"
        pygame.draw.rect(window, (255, 255, 255), back_button, 3)
        window.blit(back_text, (back_button.x + (back_button.width - back_text.get_width()) // 2, back_button.y + (back_button.height - back_text.get_height()) // 2))

        for button, text in game_mode_buttons:
            pygame.draw.rect(window, (255, 255, 255), button, 3)
            window.blit(text, (button.x + (button.width - text.get_width()) // 2, button.y + (button.height - text.get_height()) // 2))

        pygame.display.update()


# Charger l'image de fond
background = pygame.image.load("Imgs/testfond.png")

# Charger le logo
logo = pygame.image.load("Imgs/testlogo.png")

buttonBis = pygame.image.load("Imgs/testbutton.png")
buttonQuitBis = pygame.image.load("Imgs/button2.png")
buttonSoloBis = pygame.image.load("Imgs/boutton_solo.png")

button = pygame.transform.scale(buttonBis, (200, 80))
buttonQuit = pygame.transform.scale(buttonQuitBis, (200, 80))
buttonSolo = pygame.transform.scale(buttonSoloBis, (200, 80))

# Définir les dimensions et la position du logo
logo_width = 1036
logo_height = 216
logo_x = (SCREEN_WIDTH - logo_width) // 2
logo_y = 70

# Charger la police pour le bouton
font = pygame.font.SysFont("Arial", 50)

# Créer le texte pour le bouton
text = font.render("Play", True, (255, 255, 255))

button_width = 200
button_height = 80
button_x = (SCREEN_WIDTH - button_width) // 2
button_y = logo_y + logo_height + 100

#Créer le bouton solo
textSolo = font.render("Solo", True, (255, 255, 255))

buttonSolo_width = 200
buttonSolo_height = 80
buttonSolo_x = (SCREEN_WIDTH - buttonSolo_width) // 2
buttonSolo_y = logo_y + logo_height + 200

# Créer le bouton quit

buttonQuit_width = 200
buttonQuit_height = 80
buttonQuit_x = (SCREEN_WIDTH - buttonQuit_width) // 2
buttonQuit_y = logo_y + logo_height + 300

# Popup pour demander le pseudo

def show_servers(window, welcomemsg):
    font = pygame.font.SysFont("Arial", 30)

    server_buttons = []
    join_buttons = []

    for i in range(5):
        server_button_y = server_button_start_y + i * server_button_spacing

        server_text = font.render(f"Server {i + 1} (0/2)", True, (255, 255, 255))
        server_button = pygame.Rect(button_x, server_button_y, server_button_width, server_button_height)
        join_text = font.render("Rejoindre", True, (255, 255, 255))
        join_button = pygame.Rect(button_x + server_button_width + 50, server_button_y + (server_button_height - server_button_join_height) // 2, server_button_join_width, server_button_join_height)

        server_buttons.append((server_button, server_text))
        join_buttons.append((join_button, join_text))

    # Ajouter un bouton "précédent"
    back_text = font.render("Précédent", True, (255, 255, 255))
    back_button_width = 150
    back_button_height = 50
    back_button_x = 50
    back_button_y = 50
    back_button = pygame.Rect(back_button_x, back_button_y, back_button_width, back_button_height)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Vérifier si le bouton "Précédent" est cliqué
                if back_button.collidepoint(mouse_pos):
                    print("Le bouton Précédent a été cliqué !")
                    window.fill((0, 0, 0))
                    pygame.display.update()
                    return  # retourner à la fonction précédente

                for i, (join_button, _) in enumerate(join_buttons):
                    if join_button.collidepoint(mouse_pos):
                        print(f"Le bouton Rejoindre du serveur {i + 1} a été cliqué !")
                        window.fill((0, 0, 0))
                        pygame.display.update()

                        mainSolo("Online", "Mots")
                        running = False
                        break

        window.blit(background, (0, 0))

        # Afficher le bouton "Précédent"
        pygame.draw.rect(window, (255, 255, 255), back_button, 3)
        window.blit(back_text, (back_button.x + (back_button.width - back_text.get_width()) // 2, back_button.y + (back_button.height - back_text.get_height()) // 2))

        for server_button, server_text in server_buttons:
            pygame.draw.rect(window, (255, 255, 255), server_button, 3)
            window.blit(server_text, (server_button.x + (server_button.width - server_text.get_width()) // 2, server_button.y + (server_button.height - server_text.get_height()) // 2))

        for join_button, join_text in join_buttons:
            pygame.draw.rect(window, (255, 255, 255), join_button, 3)
            window.blit(join_text, (join_button.x + (join_button.width - join_text.get_width()) // 2, join_button.y + (join_button.height - join_text.get_height()) // 2))
        pygame.display.update()


    font = pygame.font.SysFont("Arial", 30)

    server_buttons = []
    join_buttons = []

    for i in range(5):
        server_button_y = server_button_start_y + i * server_button_spacing

        server_text = font.render(f"Server {i + 1} (0/2)", True, (255, 255, 255))
        server_button = pygame.Rect(button_x, server_button_y, server_button_width, server_button_height)
        join_text = font.render("Rejoindre", True, (255, 255, 255))
        join_button = pygame.Rect(button_x + server_button_width + 50, server_button_y + (server_button_height - server_button_join_height) // 2, server_button_join_width, server_button_join_height)

        server_buttons.append((server_button, server_text))
        join_buttons.append((join_button, join_text))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, (join_button, _) in enumerate(join_buttons):
                    if join_button.collidepoint(mouse_pos):
                        print(f"Le bouton Rejoindre du serveur {i + 1} a été cliqué !")
                        window.fill((0, 0, 0))
                        pygame.display.update()

                        main(i+1,"Online")
                        running = False
                        break

        window.blit(background, (0, 0))

        for server_button, server_text in server_buttons:
            pygame.draw.rect(window, (255, 255, 255), server_button, 3)
            window.blit(server_text, (server_button.x + (server_button.width - server_text.get_width()) // 2, server_button.y + (server_button.height - server_text.get_height()) // 2))

        for join_button, join_text in join_buttons:
            pygame.draw.rect(window, (255, 255, 255), join_button, 3)
            window.blit(join_text, (join_button.x + (join_button.width - join_text.get_width()) // 2, join_button.y + (join_button.height - join_text.get_height()) // 2))

        pygame.display.update()


# Boucle principale du jeu
while True:
    # Gérer les événements
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
                print("L'adresse IP saisie est :", ip)
                SERVER_HOST = "localhost"
                SERVER_PORT = 8080
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try :
                    client_socket.connect((SERVER_HOST, SERVER_PORT))
                    valueWelcome = "hello"
                    client_socket.sendall((valueWelcome + "\n").encode())
                    try:
                        welcomeMessage = client_socket.recv(1024)
                        welcomemsg = welcomeMessage.decode()
                        print(welcomemsg)
                        show_servers(window, welcomemsg)
                    except socket.timeout:
                        print("Timeout: No response received in 4 seconds. Disconnecting...")
                    #wait for server to send welcome message
                    welcomeMessage = client_socket.recv(1024)
                    print(welcomeMessage.decode())
                except :
                    print("Impossible de se connecter au serveur. Retour au menu principal.")
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

    # Afficher l'image de fond
    window.blit(background, (0, 0))

    # Afficher le logo
    window.blit(logo, (logo_x, logo_y + logo_y_offset))

    # Afficher l'image du bouton
    window.blit(button, (button_x, button_y))

    # Afficher l'image du bouton
    window.blit(buttonSolo, (buttonSolo_x, buttonSolo_y))

    # Afficher l'image du bouton
    window.blit(buttonQuit, (buttonQuit_x, buttonQuit_y))

    # Rafraîchir l'écran
    pygame.display.update()
    

    

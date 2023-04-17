import pygame
import math
from Main import main
from config import *
from utils import *

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

# Charger l'image de fond
background = pygame.image.load("Imgs/testfond.png")

# Charger le logo
logo = pygame.image.load("Imgs/testlogo.png")

buttonBis = pygame.image.load("Imgs/testbutton.png")
buttonQuitBis = pygame.image.load("Imgs/button2.png")

button = pygame.transform.scale(buttonBis, (200, 80))
buttonQuit = pygame.transform.scale(buttonQuitBis, (200, 80))

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
button_y = logo_y + logo_height + 150

# Créer le bouton quit

buttonQuit_width = 200
buttonQuit_height = 80
buttonQuit_x = (SCREEN_WIDTH - buttonQuit_width) // 2
buttonQuit_y = logo_y + logo_height + 250

# Popup pour demander le pseudo

def show_servers(window):
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
                        valTF = init()
                        main(valTF,i+1)
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
                show_servers(window)
            elif buttonQuit_x <= mouse_pos[0] <= buttonQuit_x + buttonQuit_width and buttonQuit_y <= mouse_pos[1] <= buttonQuit_y + buttonQuit_height:
                print("Le bouton Quit a été cliqué !")
                pygame.quit()
                quit()

    time = pygame.time.get_ticks() / 1000.0
    logo_y_offset = math.sin(time * 3) * 20

    # Afficher l'image de fond
    window.blit(background, (0, 0))

    # Afficher le logo
    window.blit(logo, (logo_x, logo_y + logo_y_offset))

    # Afficher l'image du bouton
    window.blit(button, (button_x, button_y))

    # Afficher l'image du bouton
    window.blit(buttonQuit, (buttonQuit_x, buttonQuit_y))

    # Rafraîchir l'écran
    pygame.display.update()
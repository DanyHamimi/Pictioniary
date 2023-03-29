import pygame
import math
from Main import main
from config import *
from utils import *

pygame.init()

# Définir les dimensions de l'écran
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
def ask_pseudo():
    pseudo = "guest"
    userBool = True
    while userBool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pseudo = "Guest"
                    userBool = False
                    return pseudo
                elif event.key == pygame.K_BACKSPACE:
                    pseudo = pseudo[:-1]
                    userBool = False
                    return pseudo
                else:
                    pseudo += event.unicode
        window.fill((255, 255, 255))
        font = pygame.font.SysFont("Arial", 50)
        text = font.render("Enter your nickname: " + pseudo, True, (0, 0, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        window.blit(text, text_rect)
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
                #pseudo = ask_pseudo()
                valTF = init()
                main(valTF)
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
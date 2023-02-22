import pygame
import cv2
import numpy as np

pygame.init()
width, height = 640, 480
pygame.display.set_mode((width, height))
pygame.display.set_caption("Webcam Feed")

cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert the frame to a Pygame surface
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)

    # Display the frame in the Pygame window
    pygame.display.get_surface().blit(frame, (0, 0))
    pygame.display.update()

    # Check for quit events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            pygame.quit()


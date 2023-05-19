import cv2
import numpy as np
import pygame
from PIL import Image
import tensorflow as tf
from PIL import ImageOps

from config import *


def drawLine(a, b, tmpcordX, tmpcordY, gomme):
    if tmpcordX == -1 and tmpcordY == -1:
        tmpcordX = a
        tmpcordY = b
    if (gomme):
        cv2.line(canvas, (tmpcordX, tmpcordY), (a, b), (255, 255, 255), 25)
        cv2.line(canvasToSave, (tmpcordX, tmpcordY), (a, b), (0, 0, 0), 25)
    else:
        cv2.line(canvas, (tmpcordX, tmpcordY), (a, b), (0, 0, 0), 25)
        cv2.line(canvasToSave, (tmpcordX, tmpcordY), (a, b), (0, 0, 0), 25)
    # cv2.imshow("Canvas", canvas)
    tmpcordX = a
    tmpcordY = b
    # Resize the canvas to 350x350
    # canvasBis = cv2.resize(canvas, (350, 350))
    cv2.imwrite("Imgs/canvasBis.jpg", canvasToSave)
    img = Image.open("Imgs/canvasBis.jpg")
    img = img.crop((200, 50, 550, 400))
    img.resize((350, 350))
    img.save("Imgs/canvas.jpg")


def imagePrediction():
    imgBis = cv2.imread("Imgs/canvas.jpg")[:, :, 0]
    width = 28
    height = 28
    dim = (width, height)
    imgBis = cv2.resize(imgBis, dim, interpolation=cv2.INTER_AREA)
    imgBis = np.invert(np.array([imgBis]))
    prediction = model.predict([imgBis])[0]

    index_to_letter(np.argmax(prediction))
    return np.argmax(prediction)


def preprocess_image(image_path, type):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)

    # Rotation de 90 degrés dans le sens horaire
    if (type == "Mathématiques"):
        image = cv2.flip(image, 1)
    if (type == "Mots"):
        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

    # Centrer l'image
    moments = cv2.moments(image)
    center_of_mass_x = int(moments['m10'] / moments['m00'])
    center_of_mass_y = int(moments['m01'] / moments['m00'])

    shift_x = image.shape[1] // 2 - center_of_mass_x
    shift_y = image.shape[0] // 2 - center_of_mass_y

    translation_matrix = np.float32([[1, 0, shift_x], [0, 1, shift_y]])
    image = cv2.warpAffine(image, translation_matrix,
                           (image.shape[1], image.shape[0]))

    # Redimensionner l'image
    image = cv2.resize(image, (28, 28), interpolation=cv2.INTER_AREA)
    image = cv2.flip(image, 1)
    image = np.expand_dims(image, axis=-1)

    # Normaliser l'image
    image = image.astype('float32')
    image /= 255

    return np.expand_dims(image, axis=0)


def index_to_letter(index):
    # Convertir l'index en code ASCII (A: 65, B: 66, ..., Z: 90)
    ascii_value = index + 65

    # Convertir le code ASCII en lettre
    letter = chr(ascii_value)

    return letter


objet_names = ["POMME", "LIVRE", "ECLAIR", "SERPENT", "LA TOUR EIFFEL", "BANANE", "AVION", "SEAU", "ENVELOPPE",
               "CAROTTE", "HACHE", "REVEIL", "CHAT", "ENCUME", "FLEUR", "MAIN", "LUNETTES", "PAPILLON", "TRIANGLE", "SHORTS"]


def predict(image_array, model, predict_type):
    prediction = model.predict(image_array)[0]

    # Obtenir les indices des deux plus grandes probabilités
    top_2_indices = np.argpartition(prediction, -2)[-2:]
    top_2_indices_sorted = top_2_indices[np.argsort(
        prediction[top_2_indices])][::-1]

    # Obtenir les prédictions et les probabilités correspondantes
    first_prediction = top_2_indices_sorted[0]
    first_probability = prediction[top_2_indices_sorted[0]] * 100

    second_prediction = top_2_indices_sorted[1]
    second_probability = prediction[top_2_indices_sorted[1]] * 100
    if predict_type == 'Mots':
        print(
            f"La lettre la plus probable est {index_to_letter(first_prediction)} avec une probabilité de {first_probability:.2f}%")
        print(
            f"La deuxième lettre la plus probable est {index_to_letter(second_prediction)} avec une probabilité de {second_probability:.2f}%")
        return (index_to_letter(first_prediction)).upper()
    elif predict_type == 'Pictionary':
        print(
            f"Le dessin la plus probable est {objet_names[first_prediction]} avec une probabilité de {first_probability:.2f}%")
        print(
            f"Le dessin la moins probable est {objet_names[second_prediction]} avec une probabilité de {second_probability:.2f}%")
        # return objet_names[first_prediction], "OU", objet_names[second_prediction]
        return objet_names[first_prediction]
    elif predict_type == 'Mathématiques':
        print(
            f"Le nombre le plus probable est {first_prediction} avec une probabilité de {first_probability:.2f}%")
        print(
            f"Le nombre le moins probable est {second_prediction} avec une probabilité de {second_probability:.2f}%")
        return first_prediction
    else:
        raise ValueError("predict_type doit être 'letter', 'draw' ou 'number'")


def predict_letter(image_array, model):
    prediction = model.predict(image_array)[0]

    # Obtenir les indices des deux plus grandes probabilités
    top_2_indices = np.argpartition(prediction, -2)[-2:]
    top_2_indices_sorted = top_2_indices[np.argsort(
        prediction[top_2_indices])][::-1]

    # Obtenir les lettres et les probabilités correspondantes
    first_letter = index_to_letter(top_2_indices_sorted[0])
    first_probability = prediction[top_2_indices_sorted[0]] * 100

    second_letter = index_to_letter(top_2_indices_sorted[1])
    second_probability = prediction[top_2_indices_sorted[1]] * 100

    print(
        f"La lettre la plus probable est {first_letter} avec une probabilité de {first_probability:.2f}%")
    print(
        f"La deuxième lettre la plus probable est {second_letter} avec une probabilité de {second_probability:.2f}%")

    # Return in lower case
    return first_letter.upper()


def win(type):
    window.fill((255, 255, 255))
    window.blit(background, (0, 0))
    font = pygame.font.SysFont('Arial', 100)
    if (type == "online"):
        text = font.render("Tu as gagné", True, (255, 255, 255))
    else:
        text = font.render("Partie terminée, Score :" +
                           type, True, (255, 255, 255))
    text_rect = text.get_rect(center=(1280 // 2, 720 // 2))
    window.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(1000)

from tensorflow.keras.models import load_model
import numpy as np
import cv2

# Charger le modèle sauvegardé
model = load_model('Modele.h5')

# Charger l'image à prédire
image = cv2.imread('canvas.jpg', cv2.IMREAD_GRAYSCALE)

# Prétraiter l'image pour qu'elle ait la même taille et la même forme que les images d'entraînement
image = cv2.resize(image, (28, 28))
image = image.reshape(1, 28, 28, 1).astype('float32') / 255

# Faire la prédiction
prediction = model.predict(image)

# Trouver la classe prédite
classe_predite = np.argmax(prediction)

# Afficher la classe prédite
print(f"La classe prédite est : {classe_predite}")

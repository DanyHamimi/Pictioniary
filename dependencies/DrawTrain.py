import numpy as np
import os
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D

def load_data(folder_path):
    X = []
    y = []
    label = 0
    class_to_file = {} # Ajout d'un dictionnaire pour stocker les correspondances entre les classes et les fichiers
    for file in os.listdir(folder_path):
        if file.endswith('.npy'):
            data = np.load(os.path.join(folder_path, file), allow_pickle=True)
            X.extend(data)
            y.extend([label] * len(data))
            class_to_file[label] = file # Ajoute l'association entre la classe et le nom du fichier
            label += 1
    return np.array(X), np.array(y), class_to_file

folder_path = "draw/"
X, y, class_to_file = load_data(folder_path)

# Prétraitement des données
X = X.reshape(-1, 28, 28, 1).astype('float32') / 255
y = keras.utils.to_categorical(y, num_classes=345)

# Séparer les données en ensembles d'entraînement et de test
indices = np.arange(X.shape[0])
np.random.shuffle(indices)
split_index = int(0.8 * X.shape[0])

X_train = X[indices[:split_index]]
y_train = y[indices[:split_index]]
X_test = X[indices[split_index:]]
y_test = y[indices[split_index:]]

# Créer le modèle
model = Sequential([
    Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(28, 28, 1)),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(64, kernel_size=(3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(345, activation='softmax')
])

# Compiler le modèle
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Entraîner le modèle
model.fit(X_train, y_train, batch_size=32, epochs=5, validation_split=0.1)

# Évaluer le modèle
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test loss: {loss:.4f}")
print(f"Test accuracy: {accuracy:.4f}")

# Afficher les correspondances entre les classes et les fichiers
print("\nClasses et fichiers associés :")
for label, file in class_to_file.items():
    print(f"Classe {label}: {file}")

model.save('Modele.h5')

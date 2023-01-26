import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

# load les data pour les num
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = tf.keras.utils.normalize(x_train, axis=1)
x_test = tf.keras.utils.normalize(x_test, axis=1)

#model =  tf.keras.models.Sequential()
#model.add(tf.keras.layers.Flatten(input_shape=(28,28)))
#model.add(tf.keras.layers.Dense(128,activation='relu'))
#model.add(tf.keras.layers.Dense(128,activation='relu'))
# 10 pour les 10 chiffres (0,1,..,9)
#model.add(tf.keras.layers.Dense(10,activation='softmax'))

# model.compile(optimizer='adam',loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# model.fit(x_train,y_train, epochs=500)

# model.save("number.model")




model = tf.keras.models.load_model('number.model')

loss, accuracy = model.evaluate(x_test, y_test)

print(loss)
print(accuracy) #accuracy la plus proche de 100%

digit_num =1



while os.path.isfile(f"dataset/digit{digit_num}.png"):
    try:
        img =  cv2.imread(f"dataset/digit{digit_num}.png")[:,:,0]
        width = 28
        height = 28
        dim = (width, height)
        img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        img = np.invert(np.array([img]))
        prediction = model.predict(img)
        print(f"le chiffre ici est :{np.argmax(prediction)}")
        plt.imshow(img[0], cmap=plt.cm.binary)
        plt.show()
    except:
        print("error")
    finally:
        digit_num += 1

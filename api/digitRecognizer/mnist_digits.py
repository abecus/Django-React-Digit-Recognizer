# %%
import numpy as np
import cv2
import os

from keras.models import Sequential
from keras.layers import Conv2D, Lambda, LeakyReLU
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense, Dropout
from keras.layers.normalization import BatchNormalization
from keras.optimizers import SGD


# %%
def model():
    model = Sequential()

    model.add(Lambda(standardize, input_shape=(28, 28, 1)))

    model.add(Conv2D(32, (3, 3), padding='Same'))
    model.add(BatchNormalization())
    model.add(LeakyReLU(alpha=0.25))
    model.add(Conv2D(32, (3, 3), padding='Same'))
    model.add(BatchNormalization())
    model.add(LeakyReLU(alpha=0.2))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(64, (3, 3), padding='Same'))
    model.add(BatchNormalization())
    model.add(LeakyReLU(alpha=0.25))
    model.add(Conv2D(64, (3, 3), padding='Same'))
    model.add(BatchNormalization())
    model.add(LeakyReLU(alpha=0.2))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(128, (3, 3), padding='Same'))
    model.add(BatchNormalization())
    model.add(LeakyReLU(alpha=0.2))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))

    model.add(Conv2D(64, (3, 3), padding='Same'))
    model.add(BatchNormalization())
    model.add(LeakyReLU(alpha=0.2))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))

    model.add(Flatten())
    model.add(BatchNormalization())
    model.add(Dropout(0.15))

    model.add(Dense(256))
    model.add(LeakyReLU(alpha=0.05))
    model.add(Dropout(0.15))

    model.add(Dense(128))
    model.add(LeakyReLU(alpha=0.05))
    model.add(Dropout(0.15))

    model.add(Dense(10, activation="softmax"))

    sgd = SGD(lr=0.001, decay=1e-8, momentum=0.95, nesterov=True)
    model.compile(loss="categorical_crossentropy",
                  optimizer="adam", metrics=["accuracy"])

    return model


# %%
mean, std = 33.318447, 78.567444


def standardize(x):
    return (x-mean)/std


# %%
dirname = os.path.dirname(__file__)
weight_path = os.path.join(dirname, './weights/cp-0040.ckpt')


def predict(img):
    "returns the predictions of the image"
    arc = model()
    arc.load_weights(weight_path)
    pred = arc.predict(img.reshape(1, 28, 28, 1))
    number = np.argmax(pred)
    prob = np.amax(pred)
    return (number, prob, pred)

#%%
from matplotlib import pyplot as plt
def crop_and_predict(img_path):
    img = cv2.imread(img_path, 0)
    img = 255 - cv2.resize(img, dsize=(28, 28), interpolation=cv2.INTER_CUBIC)    
    return predict(img)

# %%
if __name__ == "__main__":
    img = os.path.join(dirname, './d.jpg')
    img = cv2.imread(img, 0)
    img = 255 - cv2.resize(img, dsize=(28, 28), interpolation=cv2.INTER_CUBIC)
    print(predict(img))

# %%

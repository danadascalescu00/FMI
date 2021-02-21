#demo
import cv2 as cv
import tensorflow as tf
import tensorflow.keras.layers as layers
from tensorflow.keras.models import load_model
import os
# import SGD and Adam optimizers
from tensorflow.keras.optimizers import SGD, Adam, RMSprop
from DataSet import *

#params
network_input_size = (256, 256)
num_epochs_ = 100
batch_size_ = 1
learning_rate = 10 ** -4
model = None

# Get images
bgr_image = cv.imread("../data/img.png")
h, w, c = bgr_image.shape
# redimensionam imaginea conform parametrului network_input_size
bgr_image = cv.resize(bgr_image, network_input_size)
# convertim imaginea in reprezentarea Lab.
lab_image = cv.cvtColor(np.float32(bgr_image) / 255, cv.COLOR_BGR2LAB)
# luam canalul L.
L = lab_image[:, :, 0]
L = np.expand_dims(L, axis=2)
# luam canalale ab si le impartim la 128.
ab = lab_image[:, :, 1:] / 128

#defineste modelul
model = tf.keras.models.Sequential([
			layers.InputLayer(input_shape=(network_input_size[0], network_input_size[1], 1)),
            layers.Conv2D(filters=8, kernel_size=(3, 3), activation='relu', strides=(2, 2), padding='same'),
            layers.Conv2D(filters=8, kernel_size=(3, 3), activation='relu',  padding='same'),
            layers.Conv2D(filters=16, kernel_size=(3, 3), activation='relu',  padding='same'),
            layers.Conv2D(filters=16, kernel_size=(3, 3), activation='relu', strides=(2, 2), padding='same'),
            layers.Conv2D(filters=32, kernel_size=(3, 3), activation='relu',  padding='same'),
            layers.Conv2D(filters=32, kernel_size=(3, 3), activation='relu', strides=(2, 2), padding='same'),
            layers.UpSampling2D((2, 2)),
            layers.Conv2D(filters=32, kernel_size=(3, 3), activation='relu', padding='same'),
            layers.UpSampling2D((2, 2)),
            layers.Conv2D(filters=16, kernel_size=(3, 3), activation='relu', padding='same'),
            layers.UpSampling2D((2, 2)),
            layers.Conv2D(filters=2, kernel_size=(3, 3), activation='tanh', padding='same'),
        ])
model.summary()

# compileaza model
model.compile(optimizer='Adam', loss='mse')

#antreneaza modelul
L = L.reshape(1, network_input_size[0], network_input_size[1], 1)
ab = ab.reshape(1, network_input_size[0], network_input_size[1], 2)
model.fit(L, ab, batch_size=batch_size_, epochs=num_epochs_)

print(model.evaluate(L, ab, batch_size=batch_size_))
#print("L=",L.shape)
output = model.predict(L)
output *= 128

# Output colorizations
output_color_lab = np.zeros((network_input_size[0], network_input_size[1], 3))
output_color_lab[:,:,0] = lab_image[:, :, 0]
output_color_lab[:,:,1:] = output[0]
output_color_bgr = cv.cvtColor(np.float32(output_color_lab), cv.COLOR_LAB2BGR)*255
output_gray = cv.cvtColor(np.float32(output_color_bgr), cv.COLOR_BGR2GRAY)

cv.imwrite("../data/img_result.png", output_color_bgr)
cv.imwrite("../data/img_gray_version.png",output_gray)

#aplcia reteaua invatata pe o imagine noua de test, pe care nu a fost antrenata
test_image = cv.imread("../data/forest/test/bost102.jpg")
h, w, c = test_image.shape
# redimensionam imaginea conform parametrului network_input_size
bgr_image = cv.resize(test_image, network_input_size)
# convertim imaginea in reprezentarea Lab.
lab_image = cv.cvtColor(np.float32(bgr_image) / 255, cv.COLOR_BGR2LAB)
# luam canalul L.
L = lab_image[:, :, 0]
L = L.reshape(1, network_input_size[0], network_input_size[1], 1)
#print("L=",L.shape)
output = model.predict(L)
output *= 128
# Output colorizations
output_color_lab = np.zeros((network_input_size[0], network_input_size[1], 3))
output_color_lab[:,:,0] = lab_image[:, :, 0]
output_color_lab[:,:,1:] = output[0]
output_color_bgr = cv.cvtColor(np.float32(output_color_lab), cv.COLOR_LAB2BGR)*255
output_gray = cv.cvtColor(np.float32(output_color_bgr), cv.COLOR_BGR2GRAY)

cv.imwrite("../data/test_result.png", output_color_bgr)
cv.imwrite("../data/test_gray_version.png",output_gray)

import tensorflow as tf
import tensorflow.keras.layers as layers
from tensorflow.keras.models import load_model
import os
# import SGD and Adam optimizers
from tensorflow.keras.optimizers import SGD, Adam, RMSprop
from DataSet import *


class AeModel:

    def __init__(self, data_set: DataSet):
        self.data_set = data_set
        self.num_epochs = 100
        self.batch_size = 6
        self.learning_rate = 10 ** -4
        self.model = None
        self.checkpoint_dir = '../checkpoints_%s' % self.data_set.scene_name


    def define_the_model(self):
        # defineste autoencoderul
        self.model = tf.keras.models.Sequential([
            layers.InputLayer(input_shape=(self.data_set.network_input_size[0], self.data_set.network_input_size[1], 1)),
            layers.Conv2D(filters=64, kernel_size=(3, 3), activation='relu', strides=(2, 2), padding='same'),
            layers.Conv2D(filters=128, kernel_size=(3, 3), activation='relu', strides=(2, 2), padding='same'),
            layers.Conv2D(filters=256, kernel_size=(3, 3), activation='relu', strides=(2, 2), padding='same'),
            layers.Conv2D(filters=512, kernel_size=(3, 3), activation='relu', padding='same'),
            layers.Conv2D(filters=256, kernel_size=(3, 3), activation='relu', padding='same'),
            layers.UpSampling2D((2,2)),
            layers.Conv2D(filters=128, kernel_size=(3, 3), activation='relu', padding='same'),
            layers.UpSampling2D((2,2)),
            layers.Conv2D(filters=64, kernel_size=(3, 3), activation='relu', padding='same'),
            layers.UpSampling2D((2,2)),
            layers.Conv2D(filters=2, kernel_size=(3, 3), activation='tanh', padding='same')
        ])
        # afiseaza arhitectura modelului
        self.model.summary()


    def compile_the_model(self):
        # compilam modelul
        # defineste optimizatorul
        optimizer = Adam(self.learning_rate)
        # apeleaza functia 'compile' cu parametrii corespunzatori.
        self.model.compile(optimizer=optimizer, loss='mse')


    def train_the_model(self):
        if not os.path.exists(self.checkpoint_dir):
            os.makedirs(self.checkpoint_dir)
        # definim callback-ul pentru checkpoint
        checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(filepath=self.checkpoint_dir + '/model.{epoch:05d}.hdf5' )
        # apelam metoda 'fit' cu parametrii corespunzatori.
        self.data_set.input_training_images = self.data_set.input_training_images.reshape(len(self.data_set.input_training_images), 
                                                                                            self.data_set.network_input_size[0], 
                                                                                            self.data_set.network_input_size[1], 1)
        self.data_set.ground_truth_training_images = self.data_set.ground_truth_training_images.reshape(len(self.data_set.ground_truth_training_images), 
                                                                                                            self.data_set.network_input_size[0], 
                                                                                                            self.data_set.network_input_size[1], 2)
        self.model.fit(self.data_set.input_training_images, self.data_set.ground_truth_training_images, epochs=self.num_epochs, batch_size=self.batch_size, callbacks=[checkpoint_callback])


    def evaluate_the_model(self):
        output_video = None
        if self.data_set.color_video:
            output_video = cv.VideoWriter(self.data_set.video_output_name, self.data_set.video_extension_and_fourcc_dict["mp4"], 30, (144, 144))

        best_epoch = self.num_epochs  # puteti incerca si cu alta epoca de exemplu cu prima epoca,
                                      # sa vedeti diferenta dintre ultima epoca si prima
        # incarcam modelul
        best_model = load_model(os.path.join(self.checkpoint_dir, 'model.%05d.hdf5') % best_epoch)
        for i in range(len(self.data_set.input_test_images)):
            # prezicem canalele ab pe baza input_test_images[i]
            L = self.data_set.input_test_images[i].reshape(1, self.data_set.network_input_size[0], self.data_set.network_input_size[1], 1)
            output_image = best_model.predict(L)
            output_image *= 128
            # reconstruim reprezentarea Lab
            output_color_lab = np.zeros((self.data_set.network_input_size[0], self.data_set.network_input_size[1], 3))
            output_color_lab[:,:,0] = self.data_set.input_test_images[i].reshape(self.data_set.network_input_size[0], self.data_set.network_input_size[1])
            output_color_lab[:,:,1:] = output_image[0]
            # convertim din Lab in BGR
            pred_image = cv.cvtColor(np.float32(output_color_lab), cv.COLOR_LAB2BGR) * 255
            # convertim imaginea de input din L in 'grayscale'
            input_image = np.uint8(self.data_set.input_test_images[i] / 100 * 255)
            # imaginea ground-truth in format bgr
            gt_image = np.uint8(self.data_set.ground_truth_bgr_test_images[i])
            # pred_image este imaginea prezisa in format BGR.
            if self.data_set.color_video:
                pred_image = cv.resize(pred_image, (144, 144))
                output_video.write(np.uint8(pred_image))
            else:
                concat_images = self.concat_images(input_image, pred_image, gt_image)
                cv.imwrite(os.path.join(self.data_set.dir_output_images, '%d.png' % i), concat_images)
        
        output_video.release()


    def concat_images(self, input_image, pred, ground_truth):
        """
        :param input_image: imaginea grayscale (canalul L din reprezentarea Lab).
        :param pred: imaginea prezisa.
        :param ground_truth: imaginea ground-truth.
        :return: concatenarea imaginilor.
        """
        h, w, _ = input_image.shape
        space_btw_images = int(0.2 * h)
        image = np.ones((h, w * 3 + 2 * space_btw_images, 3)) * 255
        # add input_image
        image[:, :w] = input_image
        # add predicted
        offset = w + space_btw_images
        image[:, offset: offset + w] = pred
        # add ground truth
        offset = 2 * (w + space_btw_images)
        image[:, offset: offset + w] = ground_truth
        return np.uint8(image)
import numpy as np
import cv2 as cv
import os
import pdb
from sys import exit


class DataSet:

    def __init__(self):
        self.scene_name = 'glacier'  # numele scenei:  forest/coast/glacier
        self.training_dir = '../data/%s/training' % self.scene_name
        self.test_dir = '../data/%s/test' % self.scene_name
        self.color_video = True # pentru colorarea unui video se seteaza cu True
        self.video_filename = "C:/Users/Dana/Desktop/University/Anul 3/CV/Tema4/input_video.mp4"
        self.video_output_name = "%s_colored.mp4" % self.video_filename[:-4]
        self.video_extension_and_fourcc_dict = {'avi': cv.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                                                'mp4': 0x7634706d}
        self.video_file_dim = (0, 0)

        self.dir_output_images = '../data/output_images/%s' % self.scene_name
        if not os.path.exists(self.dir_output_images):
            os.makedirs(self.dir_output_images)

        self.network_input_size = (64, 64)  # dimensiunea imaginilor de antrenare
        self.input_training_images, self.ground_truth_training_images, self.ground_truth_bgr_training_images =\
            self.read_images(self.training_dir)

        self.input_test_images, self.ground_truth_test_images, self.ground_truth_bgr_test_images = None, None, None
        if self.color_video:
            self.input_test_images, self.ground_truth_test_images, self.ground_truth_bgr_test_images =\
                self.read_video_frames(self.video_filename)
        else:    
            self.input_test_images, self.ground_truth_test_images, self.ground_truth_bgr_test_images =\
                self.read_images(self.test_dir)
 

    def get_frames(self, video_filename):
        frames = []
        cap = cv.VideoCapture(video_filename)
        if cap.isOpened() is False:
            print('Error opening video stream or file!')
            exit(1)
        
        while cap.isOpened():
            ret, frame = cap.read()
            if ret is True:
                frames.append(frame)
            else:
                break

        cap.release()
        return frames


    def read_video_frames(self, video_filename):
        in_images = [] # imaginile de input(frame-urile), canalul L din reprezentarea Lab
        gt_images = [] # imaginile de output (ground-truth), canalele ab din reprezentarea Lab
        bgr_images = [] # imaginile in format BGR
         
        bgr_frames = self.get_frames(self.video_filename)
        self.video_file_dim = (bgr_frames[0].shape[1], bgr_frames[0].shape[0])
        for frame in bgr_frames:
            # redimensionam frame-ul conform parametrului self.network_input_size
            bgr_image = cv.resize(frame, self.network_input_size, interpolation=cv.INTER_AREA)
            bgr_images.append(bgr_image)
            # convertim imaginea in reprezentarea Lab
            lab_image = cv.cvtColor(np.float32(bgr_image) / 255, cv.COLOR_BGR2LAB)
            L = lab_image[:, :, 0]
            L = np.expand_dims(L, axis=2)
            in_images.append(L)
            gt_image = lab_image[:, :, 1:] / 128
            gt_images.append(gt_image)

        return np.array(in_images, np.float32), np.array(gt_images, np.float32), np.array(bgr_images, np.float32)            


    def read_images(self, base_dir):
        files = os.listdir(base_dir)
        in_images = []  # imaginile de input, canalul L din reprezentarea Lab.
        gt_images = []  # imaginile de output (ground-truth), canalele ab din reprezentarea Lab.
        bgr_images = []  # imaginile in format BGR.
        for file in files:
            # citim imaginea
            bgr_image = cv.imread(base_dir + "/" + file)
            # redimensionam imaginea conform parametrului self.network_input_size.
            bgr_image = cv.resize(bgr_image, self.network_input_size, interpolation=cv.INTER_AREA)
            bgr_images.append(bgr_image)
            # convertim imaginea in reprezentarea Lab.
            lab_image = cv.cvtColor(np.float32(bgr_image) / 255, cv.COLOR_BGR2LAB)
            # luam canalul L.
            L = lab_image[:, :, 0]
            L = np.expand_dims(L, axis=2)
            in_images.append(L)
            # luam canalale ab si le impartim la 128.
            gt_image = lab_image[:, :, 1:] / 128
            gt_images.append(gt_image)

        return np.array(in_images, np.float32), np.array(gt_images, np.float32), np.array(bgr_images, np.float32)
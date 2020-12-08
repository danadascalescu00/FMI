import os
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import pdb
from math import floor

from add_pieces_mosaic import *
from parameters import *


def load_pieces(params: Parameters):
    # citeste toate cele N piese folosite la mozaic din directorul corespunzator
    # toate cele N imagini au aceeasi dimensiune H x W x C, unde:
    # H = inaltime, W = latime, C = nr canale (C=1  gri, C=3 color)
    # functia intoarce pieseMozaic = matrice N x H x W x C in params
    # pieseMoziac[i, :, :, :] reprezinta piesa numarul i
    images = []
    images_names = os.listdir(params.small_images_dir)

    # citeste imaginile din director
    for image_name in images_names:
        current_image = cv.imread(params.small_images_dir + image_name, cv.IMREAD_COLOR)
        # in cazul in care imaginea de referinta este GRAYSCALE, pisele mozaicului vor fi convertite la GRAYSCALE
        if params.grayscale == True:
            for i in range(current_image.shape[0]):
                for j in range(current_image.shape[1]):
                    current_image[i, j][0] = 0.2126 * current_image[i, j][2] + 0.7152 * current_image[i, j][1] + 0.0722 * current_image[i, j][0]
                    current_image[i, j][1] = 0.2126 * current_image[i, j][2] + 0.7152 * current_image[i, j][1] + 0.0722 * current_image[i, j][0]
                    current_image[i, j][2] = 0.2126 * current_image[i, j][2] + 0.7152 * current_image[i, j][1] + 0.0722 * current_image[i, j][0]

        images.append(current_image)
    images = np.float32(np.array(images))
        
    if params.show_small_images:
        for i in range(10):
            for j in range(10):
                plt.subplot(10, 10, i * 10 + j + 1)
                # OpenCV reads images in BGR format, matplotlib reads images in RBG format
                im = images[i * 10 + j].copy()
                # BGR to RGB, swap the channels
                im = im[:, :, [2, 1, 0]]
                plt.imshow(im)
        plt.show()

    params.small_images = images


def compute_dimensions(params: Parameters):
    # calculeaza dimensiunile mozaicului
    # obtine si imaginea de referinta redimensionata avand aceleasi dimensiuni
    # ca mozaicul

    # calculeaza automat numarul de piese pe verticala
    aspect_ratio = params.width / params.height
    piece_height, piece_width = params.small_images.shape[1], params.small_images.shape[2]
    params.num_pieces_vertical = int(floor((aspect_ratio**(-1) * params.num_pieces_horizontal * piece_width) / piece_height))

    # redimensioneaza imaginea
    new_h = params.num_pieces_vertical * piece_height
    new_w = params.num_pieces_horizontal * piece_width

    params.image_resized = np.float32(cv.resize(params.image, (new_w, new_h)))


def build_mosaic(params: Parameters):
    # incarcam imaginile din care vom forma mozaicul
    load_pieces(params)
    # calculeaza dimensiunea mozaicului
    compute_dimensions(params)

    img_mosaic = None
    if params.layout == 'caroiaj':
        if params.hexagon is True:
            img_mosaic = add_pieces_hexagon(params)
        else:
            img_mosaic = add_pieces_grid(params)
    elif params.layout == 'aleator':
        img_mosaic = add_pieces_random(params)
    else:
        print('Wrong option!')
        exit(-1)

    return img_mosaic
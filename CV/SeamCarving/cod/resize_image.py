import sys
import cv2 as cv
import numpy as np
import copy
from math import ceil

from parameters import *
from select_path import *

import pdb

def compute_energy(img):
    """
    calculeaza energia la fiecare pixel pe baza gradientului folosind ecuatia (1) din articol
    :param img: imaginea initiala
    :return:E - energia
    """
    # urmati urmatorii pasi:
    # 1. transformati imagine in grayscale
    # 2. folositi filtru sobel pentru a calcula gradientul in directia X si Y
    # 3. calculati magnitudinea pentru fiecare pixel al imaginii
    E = np.zeros((img.shape[0],img.shape[1]))
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    sobelx = cv.Sobel(img_gray,cv.CV_64F,1,0,ksize=3)
    sobely = cv.Sobel(img_gray,cv.CV_64F,0,1,ksize=3)
    E = np.abs(sobelx) + np.abs(sobely)

    return E


def show_path(img, path, color):
    new_image = img.copy()
    for row, col in path:
        new_image[row, col] = color

    E = compute_energy(img)
    new_image_E = img.copy()
    new_image_E[:,:,0] = E.copy()
    new_image_E[:,:,1] = E.copy()
    new_image_E[:,:,2] = E.copy()

    for row, col in path:
        new_image_E[row, col] = color
    cv.imshow('path img', np.uint8(new_image))
    cv.imshow('path E', np.uint8(new_image_E))
    cv.waitKey(1000)


def delete_vertical_path(img, path):
    """
    elimina drumul vertical din imagine
    :param img: imaginea initiala
    :path - drumul vertical ce trebuie eliminat
    return: updated_img - imaginea initiala din care s-a eliminat drumul vertical
    """
    updated_img = np.zeros((img.shape[0], img.shape[1] - 1, img.shape[2]), np.uint8)
    for i in range(img.shape[0]):
        col = path[i][1]
        # copiem partea din stanga
        updated_img[i, :col] = img[i, :col].copy()
        # copiem partea din dreapta
        updated_img[i, col:] = img[i, col+1:].copy()
        
    return updated_img


def decrease_width(params: Parameters, num_pixels, roi = (0, 0, 0, 0)):
    img = params.image.copy() # copiaza imaginea originala
    for i in range(num_pixels):
        print('Eliminam drumul vertical numarul %i dintr-un total de %d.' % (i+1, num_pixels))

        # calculeaza energia dupa ecuatia (1) din articol                
        E = compute_energy(img)
        if params.resize_option == 'eliminaObiect':
            # La fiecare iteratie, algoritmul elimina insiruirea de pixeli cu costul minim(suma magnitudinilor gradientilor 
            # pixelilor ce alcatuiesc drumul este minima). Pentru a forta algoritmul sa aleaga drumuri cu pixeli din 
            # regiunea selectata, vom modifica matricea de energie, adaugand pe portiunea selectata valori negative
            image_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            max_value, min_value = np.amax(image_gray), np.amin(image_gray)
            energy_mask_const = np.abs(np.sqrt(20) * (max_value - min_value) * params.image.shape[0])
            E[roi[1]:(roi[1]+roi[3]), roi[0]:(roi[0]+roi[2])] = (-1) * energy_mask_const

        path = select_path(E, params.method_select_path)
        if params.show_path:
            show_path(img, path, params.color_path)
        img = delete_vertical_path(img, path)

    cv.destroyAllWindows()
    return img


def rotate90(image):
    return np.float32(np.array(list(zip(*image[::-1]))))


def rotate90_ccw(img):
    rotated_image = [[img[i][j] for i in range(img.shape[0])] for j in range(img.shape[1]-1,-1,-1)]
    rotated_image = np.array(rotated_image)
    return rotated_image


def decrease_height(params: Parameters, num_pixels, roi=(0, 0, 0, 0)):
    img = params.image.copy() # copiaza imaginea originala
    img_rotated = rotate90(img) # roteste imaginea 90 de grade in sensul acelor de ceasornic
    # problema eliminarii drumurilor orizontale se transforma, dupa rotirea imaginii,
    # in cea a eliminarii drumurilor verticale
    for i in range(num_pixels):
        print('Elimina drumul orizontal %i dintr-un total de %d.' %(i+1, num_pixels))

        # calculeaza energia dupa ecuatia (1) din articol
        E = compute_energy(img_rotated)
        if params.resize_option == 'eliminaObiect':
            # La fiecare iteratie, algoritmul elimina insiruirea de pixeli cu costul minim(suma magnitudinilor gradientilor 
            # pixelilor ce alcatuiesc drumul este minima). Pentru a forta algoritmul sa aleaga drumuri cu pixeli din 
            # regiunea selectata, vom modifica matricea de energie, adaugand pe portiunea selectata valori negative
            image_gray = cv.cvtColor(img_rotated, cv.COLOR_BGR2GRAY)
            max_value, min_value = np.amax(image_gray), np.amin(image_gray)
            energy_mask_const = np.abs(np.sqrt(20) * (max_value - min_value) * params.image.shape[1])
            E[roi[0]:(roi[0]+roi[2]), (roi[1]+roi[3]):(roi[1]+roi[3]+1)] = (-1) * energy_mask_const

        path = select_path(E,params.method_select_path)
        if params.show_path:
            show_path(img_rotated,path,params.color_path)
        img_rotated = delete_vertical_path(img_rotated, path)

    cv.destroyAllWindows()    
    
    img = rotate90_ccw(img_rotated) # rotim imaginea 90 de grade in sens antiorar
    return img


def delete_object(params: Parameters, x0, y0, w, h):
    if h < w:
        resized_image = decrease_height(params, h, (x0, y0, w, h))
        return resized_image
    
    resized_image = decrease_width(params, w, (x0, y0, w, h))
    return resized_image


def resize_image(params: Parameters):

    if params.resize_option == 'micsoreazaLatime':
        # redimensioneaza imaginea pe latime
        resized_image = decrease_width(params, params.num_pixels_width)
        return resized_image

    elif params.resize_option == 'micsoreazaInaltime':
        # redimensioneaza imaginea pe inaltime
        resized_image = decrease_height(params, params.num_pixels_height)
        return resized_image
    
    elif params.resize_option == 'amplificaContinut':
        # Se aplica mai intai scalarea standard pentru marirea imaginii.
        height, width = params.image.shape[0], params.image.shape[1]
        new_height, new_width = ceil(params.factor_amplification * height), ceil(params.factor_amplification * width)
        px_rem_horizontal, px_rem_vertical = new_height - height, new_width - width
        resized_image = cv.resize(params.image, (new_width, new_height))
        # Se aplica algoritmul bazat pe programare dinamica pentru micsorarea pe inaltime, respectiv latime
        # In final se obtine o imagine cu continutul amplificat, dar cu aceleasi dimensiuni ca imaginea initiala.
        print('Elimina %d pixeli din inaltimea imagini si %d pixeli din latimea imaginii.' % (px_rem_horizontal, px_rem_vertical))
        params.image = resized_image
        resized_image = decrease_width(params, px_rem_vertical)
        params.image = resized_image
        img = decrease_height(params, px_rem_horizontal)

        return img

    elif params.resize_option == 'eliminaObiect':
        img = params.image.copy() # copiaza imaginea initiala

        # Select ROI
        print('Select the region of interest and then press SPACE or ENTER button!')
        print('Cancel the selection process by pressing c button!')
        r = cv.selectROI("Delete this object", np.uint8(img), showCrosshair=False, fromCenter=False)
        cv.destroyAllWindows()

        if r == (0, 0, 0, 0):
            print('Nothing was selected!')
            return np.uint8(img)

        resized_image = delete_object(params, r[0], r[1], r[2], r[3])
        return resized_image

    else:
        print('The option is not valid!')
        sys.exit(-1)
from parameters import *
from math import floor, ceil
import numpy as np
import pdb
import timeit


def get_sorted_indexes(mean_color_pieces, mean_color_patch):
    distances = np.linalg.norm((mean_color_pieces - mean_color_patch), ord=2, axis=1)
    return distances.argsort()


def add_pieces_grid(params: Parameters):
    start_time = timeit.default_timer()

    img_mosaic = np.zeros(params.image_resized.shape, np.uint8)
    N, H, W, C = params.small_images.shape
    h, w, c = params.image_resized.shape
    num_pieces = params.num_pieces_vertical * params.num_pieces_horizontal

    if params.criterion == 'aleator':
        for i in range(params.num_pieces_vertical):
            for j in range(params.num_pieces_horizontal):
                index = np.random.randint(low=0, high=N, size=1)
                img_mosaic[i * H: (i + 1) * H, j * W: (j + 1) * W, :] = params.small_images[index]
                print('Building mosaic %.2f%%' % (100 * (i * params.num_pieces_horizontal + j + 1) / num_pieces))

    elif params.criterion == 'distantaCuloareMedie':
        small_images_means = np.array(np.mean(params.small_images, axis=(1, 2)))

        # matricea in care retinem asezarea pieselor mozaicului in caroiaj
        indexes_grid = np.zeros(shape=(params.num_pieces_horizontal, params.num_pieces_vertical)) - 1

        for i in range(params.num_pieces_vertical):
            for j in range(params.num_pieces_horizontal):
                patch = params.image_resized[i * H: (i + 1) * H, j * W: (j + 1) * W, :].copy()
                patch_mean_color = np.mean(patch, axis=(0, 1))
                sorted_indexes = get_sorted_indexes(small_images_means, patch_mean_color)
                index = 0

                if params.neighbours == True:
                    if j == 0 and i >= 1:
                        if indexes_grid[j][i - 1] == sorted_indexes[index]:
                            index = 1
                    if i == 0 and j >= 1:
                        if indexes_grid[j - 1][i] == sorted_indexes[index]:
                            index = 1
                    if j > 0 and i > 0:
                        if indexes_grid[j][i - 1] == sorted_indexes[index]:
                            index += 1
                        if indexes_grid[j - 1][i] == sorted_indexes[index]:
                            index += 1

                    indexes_grid[j][i] = sorted_indexes[index]

                img_mosaic[i * H: (i + 1) * H, j * W: (j + 1) * W, :] = params.small_images[sorted_indexes[index]]
                print('Building mosaic %.2f%%' % (100 * (i * params.num_pieces_horizontal + j + 1) / num_pieces))

    else:
        print('Error! unknown option %s' % params.criterion)
        exit(-1)

    end_time = timeit.default_timer()
    print('Running time: %f s.' % (end_time - start_time))

    return img_mosaic


def add_pieces_random(params: Parameters):
    start_time = timeit.default_timer()

    img_mosaic = np.zeros(params.image_resized.shape, np.uint8)
    N, H, W, C = params.small_images.shape
    h, w, c = params.image_resized.shape
    small_images_means = np.array(np.mean(params.small_images, axis=(1, 2)))

    # free_pixels reprzinta un "pool" de candidati(pixeli liberi, nealesi din imaginea de referinta)
    # se va alege aleator o pozitie(stanga-sus) pentru asezarea piesei in imaginea rezultat de tip mozaic
    free_pixels = np.array([[i * (w - W) + j for j in range(w - W)] for i in range(h - H)])
    while True:
        free_ = free_pixels[free_pixels > - 1]
        if len(free_) == 0:
            break

        rnd_index = np.random.randint(low=0, high=len(free_), size=1)
        row = int(free_[rnd_index] / free_pixels.shape[1])
        col = int(free_[rnd_index] % free_pixels.shape[1])

        patch = params.image_resized[row:row + H, col:col+W, :].copy()
        patch_mean_color = np.mean(patch, axis=(0, 1))
        index = get_sorted_indexes(small_images_means, patch_mean_color)[0]   

        img_mosaic[row:row + H, col:col+W, :] = params.small_images[index]

        # ne asiguram ca nu raman pixeli neacoperiti
        if row >= (h - 2 * H) and row < (h - H - 1):
            if col >= (w - 2 * W) and col < (w - W - 1):
                free_pixels[row:h-H-1, col:w-W-1] = -1
            else:
                free_pixels[row:h-H-1, col:col+W] = -1
        elif col >= (w - 2 * W) and col < (w - W - 1):
            free_pixels[row:row+H, col:w-W-1] = -1
        else:
            free_pixels[row:row+H, col:col+W] = -1

    end_time = timeit.default_timer()
    print('Running time: %f s.' % (end_time - start_time))

    return np.uint8(img_mosaic)


def add_pieces_hexagon(params: Parameters):
    start_time = timeit.default_timer()

    n, h, w, c = params.small_images.shape
    H, W, C = params.image_resized.shape
    small_images_means = np.array(np.mean(params.small_images, axis=(1, 2)))

    # construim masca hexagonala pentru piesele mozaicului
    mask = np.full((h, w, c), 1, np.uint8)
    x, y = floor(h/2), floor(w/3)
    for i in range(0, x):
        for j in range(0, y):
            if i <= j:
                mask[i, y - j - 1, :] = 0
                mask[i, 2 * y + j + 1:, :] = 0
            if i > j:
                mask[x + i, j, :] = 0
                mask[x + i, -j - 1, :] = 0

    img_mosaic = np.zeros((H + 2 * x, W  + 2 * y, C), np.uint8)

    # construim o imagine mai mare egala cu dimensiunea imaginii de referinta la care
    # se adauga un padding la fiecare margine
    bigger_image = np.zeros((H + 2 * x, W  + 2 * y, C))
    bigger_image[x:H+x, y:W+y, :] = params.image_resized.copy()

    # pentru cazul in care se doreste sa nu existe piese adiacente identice, construim 
    # o matrice in care retinem vecinii pentru fiecare piesa hexagonala; numarul de piese 
    # atat pe orizontala, cat si pe verticala va fi calculat folosind dimensiunile imaginii 
    # la care s-a adaugat padding-ul(bigger_image) si dimensiunile unei piese ale mozaicului
    num_hexagonal_pieces_horizontal =  ceil((W  + 2 * w) / w)
    num_hexagonal_pieces_vertical = ceil((H + 2 * h) / h)

    # matricea in care retinem asezarea pieselor hexagonale ale mozaicului in caroiaj
    indexes_grid = np.zeros((2 * num_hexagonal_pieces_vertical, 2 * num_hexagonal_pieces_horizontal)) - 1


    row_index = 1
    for i in range(x, bigger_image.shape[0] - h, h):
        col_index = 0
        for j in range(0, bigger_image.shape[1] - w, 4 * y):
            patch = bigger_image[i:i+h, j:j+w, :].copy()
            patch_mean_color = np.mean(patch, axis=(0, 1))
            sorted_indexes = get_sorted_indexes(small_images_means, patch_mean_color)
            index = 0

            if params.neighbours == True:
                # pentru coloane pare se verifica doar vecinul de deasupra, intrucat ele sunt primele
                # asezate pe caroiaj, exceptand prima piesa care este pe randul 1 si coloana 0
                if row_index > 1 and col_index >= 0:
                    index_neighbor = indexes_grid[row_index - 2][col_index]
                    if indexes_grid[row_index - 2][col_index] == sorted_indexes[index]:
                        index += 1

            indexes_grid[row_index][col_index] = sorted_indexes[index]
                                        
            img_mosaic[i:i+h, j:j+w, :] = (1 - mask) * img_mosaic[i:i+h, j:j+w, :] + mask * params.small_images[sorted_indexes[index]]

            col_index += 2
        row_index += 2

    row_index = 0
    for i in range(0, bigger_image.shape[0] - h, h):
        col_index = 1
        for j in range(2*y, bigger_image.shape[1] - w, 4 * y):
            patch = bigger_image[i:i+h, j:j+w, :].copy()
            patch_mean_color = np.mean(patch, axis=(0, 1))
            sorted_indexes = get_sorted_indexes(small_images_means, patch_mean_color)
            index = 0

            if params.neighbours == True:
                if row_index == 0:
                    # stanga-jos
                    if indexes_grid[row_index + 1][col_index - 1] == sorted_indexes[index]:
                        index += 1
                else:
                    # stanga-sus
                    if indexes_grid[row_index - 1][col_index - 1] == sorted_indexes[index]:
                        index += 1
                    # stanga-jos
                    if indexes_grid[row_index + 1][col_index - 1] == sorted_indexes[index]:
                        index += 1
                    # dreapta-sus 
                    if indexes_grid[row_index - 1][col_index + 1] == sorted_indexes[index]:
                        index += 1
                    # dreapta-jos
                    if indexes_grid[row_index + 1][col_index + 1] == sorted_indexes[index]:
                        index += 1
                    # sus
                    if indexes_grid[row_index - 2][col_index] == sorted_indexes[index]:
                        index += 1


            indexes_grid[row_index][col_index] = sorted_indexes[index]
            print(row_index, col_index)

            img_mosaic[i:i+h, j:j+w, :] = (1 - mask) * img_mosaic[i:i+h, j:j+w, :] + mask * params.small_images[sorted_indexes[index]]

            col_index += 2
        row_index += 2


    end_time = timeit.default_timer()
    print('Running time: %f s.' % (end_time - start_time))

    # se extrage padding-ul adaugat pentru a obtine imaginea de tip mozaic
    return img_mosaic[x:H+x, y:W+y, :]
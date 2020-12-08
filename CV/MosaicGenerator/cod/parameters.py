import cv2 as cv
import numpy as np


# In aceasta clasa vom stoca detalii legate de algoritm si de imaginea pe care este aplicat.
class Parameters:

    def __init__(self, image_path):
        self.image_path = image_path
        self.image = np.float32(cv.imread(image_path, cv.IMREAD_COLOR))
        if self.image is None:
            print('%s is not valid' % image_path)
            exit(-1)

        self.height = self.image.shape[0]
        self.width = self.image.shape[1]
        self.channels = self.image.shape[2]
        self.grayscale = False
        self.image_resized = None
        self.small_images_dir = './../data/colectie/'
        self.image_type = 'png'
        self.num_pieces_horizontal = 100
        self.num_pieces_vertical = None
        self.show_small_images = False
        self.layout = 'caroiaj'
        self.criterion = 'aleator'
        self.hexagon = False
        self.small_images = None
        self.neighbours = False

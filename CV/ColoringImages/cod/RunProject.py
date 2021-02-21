"""
    PROIECT
    Colorarea imaginilor folosind autoencoder.
"""

import pdb
from DataSet import *
from AeModel import *


data_set: DataSet = DataSet()
ae_model: AeModel = AeModel(data_set)

ae_model.define_the_model()
ae_model.compile_the_model()
ae_model.train_the_model()
ae_model.evaluate_the_model()
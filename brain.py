import tensorflow as tf
import numpy as np

class DNA:
    def __init__(self):
        pass

    def _setDNA(self):
        pass

    def _setRandomDNA(self):
        pass

class Brain(DNA):
    def __init__(self, layers, weights=None):
        if not weights:
            self._model = tf.keras.Sequential([
                tf.keras.layers.InputLayer(input_shape=(4,)),
                tf.keras.layers.Dense(8, input_shape=(4,), activation='sigmoid'),
                tf.keras.layers.Dense(3, activation='sigmoid')
            ])
        self._setDNA()


layers = [4, 8, 3]
brain = Brain(layers)
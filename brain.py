import tensorflow as tf
import numpy as np

class DNA:
    def __init__(self, layers, weights):
        self._layers = layers
        self._weights = weights
        self._setDNA()
        print(self._weights)

    def _setDNA(self):
        # not self._weights = set random weights
        if not self._weights:
            self._weights = []
            for i in range(len(layers) - 1):
                inputs = layers[i]
                outputs = layers[i + 1]
                weights = np.random.uniform(-1, 1, (inputs, outputs))
                biases = np.zeros(outputs)
                new = np.array([weights, biases])
                self._weights.append(new)
        else:
            pass

class Brain(DNA):
    def __init__(self, layers, weights=None):
        super(Brain, self).__init__(layers, weights)
        self._model = tf.keras.Sequential([
            tf.keras.layers.InputLayer(input_shape=(4,)),
            tf.keras.layers.Dense(8, input_shape=(4,), activation='sigmoid'),
            tf.keras.layers.Dense(3, activation='sigmoid')
        ])

layers = [4, 8, 3]
brain = Brain(layers)
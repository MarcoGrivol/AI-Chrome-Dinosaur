import tensorflow as tf
import numpy as np

class DNA:
    def __init__(self, weights):
        self._weights = weights
        # self._setDNA()

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
        self.fitness = 0
        self._layers = layers
        self._model = tf.keras.Sequential()
        self._addLayersToModel()
        # if random weights
        if not weights:
            weights = []
            for data in self._model.layers:
                weights.append(data.get_weights())
            weights = np.array(weights)
        super(Brain, self).__init__(weights)

    def _addLayersToModel(self):
        new = tf.keras.layers.InputLayer(input_shape=(self._layers[0],))
        self._model.add(new)
        # ignore the input layers defined above with range starting at 1
        for i in range(1, len(self._layers)):
            new = tf.keras.layers.Dense(self._layers[i], activation='tanh')
            self._model.add(new)

    def runInputs(self, inputs):
        data = np.array(inputs)
        data = data.transpose()
        # return outputs
        # predict return numpy.ndarray
        return self._model.predict(data)[0][0]
        

if __name__ == "__main__":
    from web import Game

    layers = [4, 8, 1]
    brain = Brain(layers)

    game = Game()
    score, outputs = game.play(brain)
    print(outputs, len(outputs), type(outputs))
    print(outputs.astype(float))
    print(outputs[0][0])
    
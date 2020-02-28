from brain import Brain

class Population:
    # each element in layers represent a layer and the element represent the number of neurons inside each layer
    # layers = [4, 8, 3] represents 4 inputs, 1 hidden layer with 8 neurons and output 3 outputs
    def __init__(self, popSize, layers):
        self._popSize = popSize
        self._layers = layers
        self._population = []

        for i in range(popSize):
            self._population.append(Brain(self._layers))
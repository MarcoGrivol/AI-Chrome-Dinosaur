from brain import Brain
from web import Game

class Population:
    # each element in layers represent a layer and the element represent the number of neurons inside each layer
    # layers = [4, 8, 3] represents 4 inputs, 1 hidden layer with 8 neurons and output 3 outputs
    def __init__(self, popSize, layers):
        self._game = Game()
        self._popSize = popSize
        self._layers = layers
        self._population = []
        for _ in range(popSize):
            self._population.append(Brain(self._layers))
    
    def runGame(self):
        for i in range(self._popSize):
            score =  self._game.play(self._population[i])
            self._population[i].fitness = score
            print("--------------------------------------------------------------------------")
            print(i, self._population[i].fitness)
            print("--------------------------------------------------------------------------")

if __name__ == "__main__":
    popSize = 10
    layers = [5, 8, 4, 1]
    population = Population(popSize, layers)
    population.runGame()
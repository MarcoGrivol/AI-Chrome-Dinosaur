from brain import Brain
from web import Game
import random
import math

class Population:
    # each element in layers represent a layer and the element represent the number of neurons inside each layer
    # layers = [4, 8, 3] represents 4 inputs, 1 hidden layer with 8 neurons and output 3 outputs
    def __init__(self, popSize, layers):
        # self._game = Game()
        self._popSize = popSize
        self._layers = layers
        self._population = []
        for _ in range(popSize):
            self._population.append(Brain(self._layers))
    
    def runGeneration(self):
        for i in range(self._popSize):
            score =  self._game.play(self._population[i])
            self._population[i].fitness = score
            print("--------------------------------------------------------------------------")
            print(i, self._population[i].fitness)
            print("--------------------------------------------------------------------------")

    def _coinToss(self):
        return random.randint(0, 1)

    def _zeroMeanFitness(self):
        # mean = 0
        # fitnessList = []
        # for member in self._population:
        #     mean += member.fitness
        #     fitnessList.append(member.fitness)
        # mean /= self._popSize
        # fitnessList = [int(math.ceil(score - mean)) for score in fitnessList]
        # return fitnessList
        pop = [170.0, 63.0, 104.0, 48.0, 48.8, 48.0, 133.0, 61.0, 57.0, 90.0]
        mean = 0
        fitnessList = []
        for member in pop:
            mean += member
            fitnessList.append(member)
        mean /= self._popSize
        fitnessList = [int(math.ceil(score - mean)) for score in fitnessList]
        return fitnessList

    # retunrs list with the best fit members
    # every member of the population is in the list, but those w better fit will repeat
    def _bestFitPopulation(self):
        fitnessList = self._zeroMeanFitness()
        popToCrossover = []
        for i in range(self._popSize):
            if fitnessList[i] > 0:
                for _ in range(fitnessList[i]):
                    popToCrossover.append(i)
            else:
                popToCrossover.append(i)
        return popToCrossover

    def _randIndex(self, a, b):
        return random.randint(a, b)

    def _mixDNA(self, parentA, parentB):
        parentA = self._population[parentA].getDNA()
        parentB = self._population[parentB].getDNA()
        dna = []
        # for weights, biases in parentA:
        #     if self._coinToss():
        #         childDNA.append(weights)
        #         childDNA.append(biases)
        #     else:
        #         pass
        print("PARENT AAAAA =============================")
        print(parentA)
        print("PARENT BBBBB =============================")
        print(parentB)
        for layer in range(len(parentA)):
            for wb in range(len(parentA[layer]) - 1):
                weightA = parentA[layer][wb] 
                biasesA = parentA[layer][wb + 1] 
                weightB = parentB[layer][wb] 
                biasesB = parentB[layer][wb + 1]                 
                for i in range(len(weightA)):
                    for j in range(len(weightA[0])):
                        
        
        print("CHILD =================================")
        print(dna)
        return dna

    def crossOver(self):
        newPopulation = []
        popToCrossover = self._bestFitPopulation()
        maxRange = len(popToCrossover) - 1
        for _ in range(1):
            indexA = random.randint(0, maxRange)
            parentA = popToCrossover[indexA]
            indexB = random.randint(0, maxRange)
            parentB = popToCrossover[indexB]
            while parentA == parentB:
                indexB = random.randint(0, maxRange)
                parentB = popToCrossover[indexB]
            dna = self._mixDNA(parentA, parentB)
            child = Brain(self._layers, weights=dna)
            newPopulation.append(child)
        self._population = newPopulation


if __name__ == "__main__":
    popSize = 10
    layers = [5, 8, 1]
    population = Population(popSize, layers)
    #  population.runGeneration()
    population.crossOver()

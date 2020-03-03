from brain import Brain
from web import Game
import random
import math
import numpy as np

class Population:
    # each element in layers represent a layer and the element represent the number of neurons inside each layer
    # layers = [4, 8, 3] represents 4 inputs, 1 hidden layer with 8 neurons and output 3 outputs
    def __init__(self, popSize, layers, mutation=0.1, leftOver=0.2):
        self._game = Game()
        self._popSize = popSize
        self._layers = layers
        self._mutation = mutation
        self._leftOver = leftOver
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

    def _fitnessFormat(self):
        fitnessList = [int(member.fitness) for member in self._population]
        # -1 to avoid empty fitness list
        minimum = min(fitnessList) - 1
        fitnessList = [n - minimum for n in fitnessList]
        return fitnessList

    # retunrs list with the best fit members
    # every member of the population is in the list, but those w better fit will repeat
    def _bestFitPopulation(self):
        fitnessList = self._fitnessFormat()
        popToCrossover = []
        for i in range(self._popSize):
            for _ in range(fitnessList[i]):
                popToCrossover.append(i)
        return popToCrossover

    def _mixDNA(self, parentA, parentB):
        parentA = self._population[parentA].getDNA()
        parentB = self._population[parentB].getDNA()
        dna = []
        for layer in range(len(parentA)):
            for wb in range(len(parentA[layer]) - 1):
                # define the weight             
                weightA = parentA[layer][wb] 
                weightB = parentB[layer][wb] 
                childWeight = []  
                for i in range(len(weightA)):
                    row = []
                    for j in range(len(weightA[0])):
                        if self._coinToss():
                            row.append(weightA[i][j])
                        else:
                            row.append(weightB[i][j])
                    childWeight.append(row)
                # define the bias
                biasA = parentA[layer][wb + 1] 
                biasB = parentB[layer][wb + 1] 
                childBias = []
                if self._coinToss():
                    childBias.append(biasA)
                else:
                    childBias.append(biasB)

            # add layer weight and bias
            dna.append([np.array(childWeight), np.array(childBias)])
        return dna

    def _isLeftOver(self):
        if self._leftOver < random.uniform(0, 1):
            fitnessList = [int(member.fitness) for member in self._population]
            minimum = min(fitnessList)
            for i in range(self._popSize):
                if self._population[i].fitness > minimum:
                    return self._population[i]
        else:
            return False

    def crossOver(self):
        newPopulation = []
        popToCrossover = self._bestFitPopulation()
        maxRange = len(popToCrossover) - 1
        print(popToCrossover, maxRange)
        for _ in range(self._popSize):
            leftOver = self._isLeftOver()
            if not leftOver:
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
            else:
                newPopulation.append(leftOver)
        self._population = newPopulation


if __name__ == "__main__":
    popSize = 8
    layers = [5, 8, 10, 1]
    population = Population(popSize, layers)
    for i in range(10):
        print("Population: ", i)
        population.runGeneration()
        population.crossOver()
        print("===============================================================")

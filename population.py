from brain import Brain
from web import Game
import random
import math
import numpy as np

class Population:
    # each element in layers represent a layer and the element represent the number of neurons inside each layer
    # layers = [4, 8, 3] represents 4 inputs, 1 hidden layer with 8 neurons and output 3 outputs
    def __init__(self, popSize, layers, generations=10, crossoverPop=0.75, leftOverPop=0.1, newPop=0.15, mutation=0.1):
        assert (crossoverPop + leftOverPop + newPop) == 1.0, "sum of crossoverPop, leftOverPop, newPop should equal 1.0" 
        self._popSize = popSize
        self._layers = layers
        self._generations = generations
        self._crossoverPop = int(crossoverPop * self._popSize)
        self._leftOverPop = int(leftOverPop * self._popSize)
        self._newPop = int(newPop * self._popSize)
        self._mutation = mutation
        self._population = []
        for _ in range(popSize):
            self._population.append(Brain(self._layers))
        self._game = Game()
        self._remaining = self._checkForWarning() 

    def _checkForWarning(self):
        if self._crossoverPop < 1:
            print("WARNING: ")
            print("    No member will be chosen for crossover. Increase the probability or the population size")
        if self._leftOverPop < 1:
            print("WARNING: ")
            print("    No member will be chosen for left over. Increase the probability or the population size")
        if self._newPop < 1:
            print("WARNING: ")
            print("    No member will be chosen for new population. Increase the probability or the population size")
        remaining = self._crossoverPop + self._leftOverPop + self._newPop
        remaining = self._popSize - remaining
        if remaining:
            print("\nWARNING: ")
            print("    Due to rounding the sum of members is less than population size, ")
            print("        the remaining {} members will be chosen from corssover.".format(remaining))
        return remaining
    
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
        fitnessList = [math.ceil((n - minimum) / 5) for n in fitnessList]
        return np.array(fitnessList)

    # retunrs list with the best fit members
    # every member of the population is in the list, but those w better fit will repeat
    def _bestFitPopulation(self):
        fitnessList = self._fitnessFormat()
        popToCrossover = []
        print("fitness list")
        print(fitnessList)
        for i in range(self._popSize):
            for _ in range(fitnessList[i]):
                popToCrossover.append(i)
        return popToCrossover

    def _isMutation(self):
        if self._mutation < random.uniform(0, 1):
            return random.uniform(-1, 1)
        else:
            return False

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
                        # if mutation then ignore parent weights
                        isMutation = self._isMutation()
                        if not isMutation:
                            # if cointoss = true choose parentA else B
                            if self._coinToss():
                                row.append(weightA[i][j])
                            else:
                                row.append(weightB[i][j])
                        else:
                            row.append(isMutation)
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
    
    def _crossOver(self):
        newPopulation = []
        popToCrossover = self._bestFitPopulation()
        maxRange = len(popToCrossover) - 1
        print(popToCrossover, maxRange)
        for _ in range(self._crossoverPop):
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
        return newPopulation

    def _leftOver(self):
        newPopulation = []
        for _ in range(self._leftOverPop):
            randIndex = random.randint(0, self._popSize - 1)
            newPopulation.append(self._population[randIndex])
        return newPopulation

    def _newPopulation(self):
        newPopulation = []
        for _ in range(self._newPop):
            new = Brain(self._layers)
            newPopulation.append(new)
        temp = self._remaining
        while self._remaining:
            new = Brain(self._layers)
            newPopulation.append(new)
            self._remaining += -1
        self._remaining = temp
        return newPopulation

    def newGeneration(self):
        newPopulation = []
        new = self._crossOver()
        newPopulation += new
        # print(new, len(new))
        new = self._leftOver()
        newPopulation += new
        # print(new, len(new))
        new = self._newPopulation()
        newPopulation += new
        # print(new, len(new))
        # print(newPopulation)
        self._population = []
        self._population = newPopulation

    def runForAallGenerations(self):
        for i in range(self._generations):
            print("Population: ", i)
            self.runGeneration()
            self.newGeneration()
            print("================================================")

if __name__ == "__main__":
    popSize = 10
    layers = [5, 8, 1]
    population = Population(popSize, layers, generations=100)
    population.runForAallGenerations()

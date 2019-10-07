from numpy import exp
import math
import random
import json

class Connection:
  def __init__(self, weight, deltaWeight = 0):
    self.weight = weight
    self.deltaWeight = deltaWeight


class Neuron:
  def __init__(self, outputsNum, index):
    self.outputWeights = [Connection(random.uniform(0, 1)) for _ in range(outputsNum)]
    self.index = index
    self.eta = .15
    self.alpha = .5
    self.output = 1

  def activation(self, x):
      # return 1 / (1 + Decimal(math.e) ** Decimal(-x))   # Sigmoid Activation
      return 1 / (1 + exp(-x))   # Sigmoid Activation
      # return math.tanh(x)           # Tanh Activation

  def activationDerivative(self, x):
      return x * (1 - x)              # Sigmoid Activation
      # return 1 - x * x              # Tanh Activation

  def feedForward(self, prevLayer):
    summary = 0
    for neuron in prevLayer:
      summary += neuron.output * neuron.outputWeights[self.index].weight

    self.output = self.activation(summary)

  def sumDOW(self, nextLayer):
    summary = 0
    for n in range(len(nextLayer) - 1):
      summary += self.outputWeights[n].weight * nextLayer[n].gradient

    return summary

  def calcOutputGradients(self, targetValue):
    self.gradient = (targetValue - self.output) * self.activationDerivative(self.output)

  def calcHiddenGradients(self, nextLayer):
    self.gradient = self.sumDOW(nextLayer) * self.activationDerivative(self.output)

  def updateWeights(self, prevLayer):
    for n in range(len(prevLayer)):
      neuron = prevLayer[n]

      newDeltaWeight = self.eta * neuron.output * self.gradient + self.alpha * neuron.outputWeights[self.index].deltaWeight

      neuron.outputWeights[self.index].deltaWeight = newDeltaWeight
      neuron.outputWeights[self.index].weight += newDeltaWeight


class NeuralNetwork:
  def __init__(self, structure = []):
    if structure == []:
      return;
    self.setStructure(structure)

  def setStructure(self, structure):
    self.layers = []
    self.avgError = 0
    self.avgSmoothingFactor = 100

    layerNum = 0
    for neuronNum in structure:
      outputsNum = 0 if layerNum == len(structure) - 1 else structure[layerNum + 1]
      self.layers.append([Neuron(outputsNum, index) for index in range(neuronNum + 1)])
      self.layers[-1][-1].output = 1.0
      layerNum += 1

  def train(self, training_inputs, training_outputs, iterations):
    for it in range(iterations):
      self.feedForward(training_inputs[it % len(training_inputs)])
      self.backProp(training_outputs[it % len(training_outputs)])

  def feedForward(self, inputs):
    for i in range(len(inputs)):
      self.layers[0][i].output = inputs[i]

    for layerNum in range(1, len(self.layers)):
      prevLayer = self.layers[layerNum - 1]
      for j in range(len(self.layers[layerNum]) - 1):
        self.layers[layerNum][j].feedForward(prevLayer)

  def backProp(self, targets):
    outputLayer = self.layers[-1]
    self.error = 0

    for i in range(len(outputLayer) - 1):
      delta = targets[i] - outputLayer[i].output
      self.error = delta * delta

    self.error /= len(outputLayer) - 1
    self.error = math.sqrt(self.error)

    self.avgError = (self.avgError * self.avgSmoothingFactor + self.error) / (self.avgSmoothingFactor + 1)

    for i in range(len(outputLayer) - 1):
      outputLayer[i].calcOutputGradients(targets[i])

    # Calculate hidden gradients
    for layerNum in reversed(range(1, len(self.layers) - 1)):
      for n in range(len(self.layers[layerNum])):
        self.layers[layerNum][n].calcHiddenGradients(self.layers[layerNum + 1])

    # Update weights
    for layerNum in reversed(range(1, len(self.layers))):
      for n in range(len(self.layers[layerNum]) - 1):
        self.layers[layerNum][n].updateWeights(self.layers[layerNum - 1])

  def saveModel(self, path):
    model = {
      "structure": [],
      "model": []
    }
    for layer in range(len(self.layers)):
      model["structure"].append(len(self.layers[layer])-1)
      model["model"].append([])
      for neuron in range(len(self.layers[layer])):
        model["model"][layer].append([])
        for conn in self.layers[layer][neuron].outputWeights:
          model["model"][layer][neuron].append({
            "weight": conn.weight,
            "deltaWeight": conn.deltaWeight
          })
    json.dump(model, open(path, "w"))

  def loadModel(self, path):
    model = json.load(open(path))
    self.setStructure(model["structure"])
    for layer in range(len(model["model"])):
      for neuron in range(len(model["model"][layer])):
        self.layers[layer][neuron].outputWeights.clear()
        self.layers[layer][neuron].outputWeights = [Connection(conn["weight"], conn["deltaWeight"]) for conn in model["model"][layer][neuron]]

  def getResults(self):
    result = []
    for n in range(len(self.layers[-1]) - 1):
      result.append(self.layers[-1][n].output)
    return result

  def test(self):
    self.setStructure([2, 4, 1])

    training_inputs = [[1, 1],
                       [1, 0],
                       [0, 1],
                       [0, 0]]

    training_outputs = [[1], [0], [0], [1]]

    self.train(training_inputs, training_outputs, 1000)

    print("Network trained. Now you can test it:")

    while 1:
      a = int(input("- a: "))
      b = int(input("  b: "))
      self.feedForward([a, b])
      print(self.getResults())
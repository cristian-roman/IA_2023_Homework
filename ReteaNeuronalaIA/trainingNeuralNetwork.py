import numpy as np

from instance import Instance

from neuralNetworkUtils import NeuralNetworkUtils


class TrainingNeuralNetwork:
    number_of_input_neurons = 7
    number_of_hidden_layers = 2
    number_of_output_neurons = 3
    learning_rate = 0.1
    max_number_of_epochs = 1000

    def __init__(self, instances: np.array(Instance)):
        self.number_of_neurons_per_hidden_layer  = int(2 / 3 * self.number_of_input_neurons + self.number_of_output_neurons)
        self.instances = instances
        self.weights_list = []
        self.initialize_weights_and_biases()

    @staticmethod
    def xavier_initialization(number_of_neurons_previous_layer, number_of_neurons_current_layer):
        variance = 1 / (number_of_neurons_previous_layer + number_of_neurons_current_layer)
        standard_deviation = np.sqrt(variance)
        weights = np.random.normal(0, standard_deviation,
                                   size=(number_of_neurons_current_layer, number_of_neurons_previous_layer + 1))
        return weights

    def initialize_weights_and_biases(self):
        np.random.seed(14)
        # Initialize 7 random weights for communication between input layer and first hidden layer
        first_hidden_layer_weights = ((TrainingNeuralNetwork.xavier_initialization
                                       (self.number_of_input_neurons, self.number_of_neurons_per_hidden_layer))
                                      .reshape(self.number_of_neurons_per_hidden_layer,
                                               self.number_of_input_neurons + 1))

        # Initialize 7 random weights for communication between first hidden layer and second hidden layer
        second_hidden_layer_weights = ((TrainingNeuralNetwork.xavier_initialization
                                        (self.number_of_neurons_per_hidden_layer,
                                         self.number_of_neurons_per_hidden_layer))
                                       .reshape(self.number_of_neurons_per_hidden_layer,
                                                self.number_of_neurons_per_hidden_layer + 1))

        # Initialize 3 random weights for communication between second hidden layer and output layer
        output_layer_weights = ((TrainingNeuralNetwork.xavier_initialization
                                 (self.number_of_neurons_per_hidden_layer, self.number_of_output_neurons))
                                .reshape(self.number_of_output_neurons, self.number_of_neurons_per_hidden_layer + 1))

        self.weights_list.append(first_hidden_layer_weights)
        self.weights_list.append(second_hidden_layer_weights)
        self.weights_list.append(output_layer_weights)

    @staticmethod
    def __reLUDerivative(x):
        if x > 0:
            return 1
        else:
            return 0

    @staticmethod
    def __softmaxDerivative(x):
        return x * (1 - x)

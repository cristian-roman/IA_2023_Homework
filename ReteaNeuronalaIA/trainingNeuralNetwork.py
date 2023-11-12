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
        self.number_of_neurons_per_hidden_layer = int(
            2 / 3 * self.number_of_input_neurons + self.number_of_output_neurons)
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

    def train(self):
        for epoch in range(self.max_number_of_epochs):
            for instance in self.instances:
                neurons = NeuralNetworkUtils.propagate_forward(instance[0].attributes, self.weights_list)
                self.back_propagate(instance[0], neurons)

    def back_propagate(self, instance: Instance, neurons: list[
        np.array(np.float32), np.array(np.float32), np.array(np.float32)]):
        # Output layer backpropagation
        output_layer = neurons[2]

        second_hidden_layer_transpose = np.transpose(neurons[1])

        softmax_derivative_with_respect_to_hidden_layer_output = [self.__softmaxDerivative(output_layer[0]),
                                                                  self.__softmaxDerivative(output_layer[1]),
                                                                  self.__softmaxDerivative(output_layer[2])]

        cost_function_derivative_with_respect_to_softmax = [self.__cross_validation_error_derivative
                                                            (instance.expected_output[0], output_layer[0]),
                                                            self.__cross_validation_error_derivative
                                                            (instance.expected_output[1], output_layer[1]),
                                                            self.__cross_validation_error_derivative(
                                                                instance.expected_output[2], output_layer[2])]

        cost_derivative_with_respect_to_second_hidden_layer_output = np.multiply(
            cost_function_derivative_with_respect_to_softmax,
            softmax_derivative_with_respect_to_hidden_layer_output)

        output_layer_delta = (self.learning_rate * np.outer
        (cost_derivative_with_respect_to_second_hidden_layer_output, second_hidden_layer_transpose))

        # Second hidden layer backpropagation
        second_hidden_layer = neurons[1]

        first_hidden_layer_transpose = np.transpose(neurons[1])

        second_hidden_layer_output_derivative_with_respect_to_reLU = self.weights_list[2]

        reLU_derivative_with_respect_to_first_hidden_layer_output = [self.__reLUDerivative(second_hidden_layer[0]),
                                                                     self.__reLUDerivative(second_hidden_layer[1]),
                                                                     self.__reLUDerivative(second_hidden_layer[2]),
                                                                     self.__reLUDerivative(second_hidden_layer[3]),
                                                                     self.__reLUDerivative(second_hidden_layer[4]),
                                                                     self.__reLUDerivative(second_hidden_layer[5]),
                                                                     self.__reLUDerivative(second_hidden_layer[6]),
                                                                     self.__reLUDerivative(second_hidden_layer[7])]

        cost_derivative_with_respect_to_first_hidden_layer_output = np.multiply(
            np.multiply(cost_derivative_with_respect_to_second_hidden_layer_output,
                        second_hidden_layer_output_derivative_with_respect_to_reLU),
            reLU_derivative_with_respect_to_first_hidden_layer_output)

        second_hidden_layer_delta = (
                self.learning_rate * np.outer(cost_derivative_with_respect_to_first_hidden_layer_output,
                                              first_hidden_layer_transpose))

        # First hidden layer backpropagation
        first_hidden_layer = neurons[0]

        input_with_bias = np.append(instance.attributes, 1)  # bias added on the last position

        first_hidden_layer_output_derivative_with_respect_to_reLU = self.weights_list[1]

        reLU_derivative_with_respect_to_input = [self.__reLUDerivative(first_hidden_layer[0]),
                                                 self.__reLUDerivative(first_hidden_layer[1]),
                                                 self.__reLUDerivative(first_hidden_layer[2]),
                                                 self.__reLUDerivative(first_hidden_layer[3]),
                                                 self.__reLUDerivative(first_hidden_layer[4]),
                                                 self.__reLUDerivative(first_hidden_layer[5]),
                                                 self.__reLUDerivative(first_hidden_layer[6]),
                                                 self.__reLUDerivative(first_hidden_layer[7])]
        cost_derivative_with_respect_to_input = np.multiply(np.multiply(
            cost_derivative_with_respect_to_first_hidden_layer_output,
            first_hidden_layer_output_derivative_with_respect_to_reLU),
            reLU_derivative_with_respect_to_input)

        first_hidden_layer_delta = (
                    self.learning_rate * np.outer(cost_derivative_with_respect_to_input, input_with_bias))

        # Update weights
        self.weights_list[0] -= first_hidden_layer_delta
        self.weights_list[1] -= second_hidden_layer_delta
        self.weights_list[2] -= output_layer_delta

    # @staticmethod
    # def __cross_validation_error(instance_output_distribution, propagated_output_distribution):
    #     error = 0
    #     for i in range(len(instance_output_distribution)):
    #         error += instance_output_distribution[i] * np.log(propagated_output_distribution[i])
    #     return error

    @staticmethod
    def __cross_validation_error_derivative(specific_instance_output, specific_softmax_output):
        return specific_instance_output / specific_softmax_output

    @staticmethod
    def __softmaxDerivative(specific_raw_output: np.float32):  # raw_output is the value of softmax applied in a
        # specific point
        return specific_raw_output * (1 - specific_raw_output)

    @staticmethod
    def __reLUDerivative(x):
        if x > 0:
            return 1
        else:
            return 0

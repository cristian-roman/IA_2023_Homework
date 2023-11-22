import numpy as np

from instance import Instance

from neuralNetworkUtils import NeuralNetworkUtils as NNU


class TrainingNeuralNetwork:
    total_input_neurons = 7
    total_hidden_layers = 2
    total_output_neurons = 3
    learning_rate = 0.1
    max_epochs = 1000

    def __init__(self, instances: np.array(Instance)):
        hidden_layer_neurons_ratio = 2 / 3
        self.total_neurons_per_hidden_layer = int(
            hidden_layer_neurons_ratio * self.total_input_neurons + self.total_output_neurons)

        self.instances = instances
        self.weights_list = []
        self.biases_list = []
        self.initialize_weights_and_biases()

    def initialize_weights_and_biases(self):
        first_hidden_layer_weights = NNU.he_initialization(self.total_input_neurons,
                                                           self.total_neurons_per_hidden_layer)
        first_hidden_layer_biases = np.random.randn(self.total_neurons_per_hidden_layer, 1) * 0.01

        second_hidden_layer_weights = NNU.he_initialization(self.total_neurons_per_hidden_layer,
                                                            self.total_neurons_per_hidden_layer)
        second_hidden_layer_biases = np.random.randn(self.total_neurons_per_hidden_layer, 1) * 0.01

        output_layer_weights = NNU.he_initialization(self.total_neurons_per_hidden_layer,
                                                     self.total_output_neurons)
        output_layer_biases = np.random.randn(self.total_output_neurons, 1) * 0.01

        self.weights_list.append(first_hidden_layer_weights)
        self.weights_list.append(second_hidden_layer_weights)
        self.weights_list.append(output_layer_weights)

        self.biases_list.append(first_hidden_layer_biases)
        self.biases_list.append(second_hidden_layer_biases)
        self.biases_list.append(output_layer_biases)

    def train(self):
        for epoch in range(self.max_epochs):
            for instance in self.instances:
                neurons = NNU.propagate_forward(instance[0].attributes, self.weights_list, self.biases_list)

                # back propagate
                d_softmax = NNU.d_softmax(neurons[5])
                cost_gradient = NNU.cost_gradient(instance[0].expected_output, neurons[5])
                o_gradient = self.get_output_gradient(d_softmax, cost_gradient)

                rh2 = neurons[3]
                delta_w3 = self.learning_rate * np.dot(o_gradient, rh2.reshape(1, -1))
                delta_b3 = self.learning_rate * o_gradient

                h2 = neurons[2]
                d_relu2 = NNU.d_reLU(h2)
                rh2_gradient = self.get_rh2_gradient(d_relu2, o_gradient)

                rh1 = neurons[1]
                delta_w2 = self.learning_rate * np.dot(rh2_gradient, rh1.reshape(1, -1))
                delta_b2 = self.learning_rate * rh2_gradient

                h1 = neurons[0]
                d_relu1 = NNU.d_reLU(h1)
                rh1_gradient = self.get_rh1_gradient(d_relu1, rh2_gradient)

                instance_input = instance[0].attributes
                delta_w1 = self.learning_rate * np.dot(rh1_gradient, instance_input.reshape(1, -1))
                delta_b1 = self.learning_rate * rh1_gradient

                self.weights_list[0] += delta_w1
                self.weights_list[1] += delta_w2
                self.weights_list[2] += delta_w3

                self.biases_list[0] += delta_b1
                self.biases_list[1] += delta_b2
                self.biases_list[2] += delta_b3

    def get_output_gradient(self, d_softmax, cost_gradient):
        output_gradient = []
        for i in range(self.total_output_neurons):
            output_gradient.append(d_softmax[i][0] * cost_gradient[i][0])

        return np.array(output_gradient).reshape(-1, 1)

    def get_rh2_gradient(self, d_relu2, o_gradient):
        rh2_gradient = []
        w2T = np.transpose(self.weights_list[2])
        for j in range(self.total_neurons_per_hidden_layer):
            sum = 0
            for k in range(self.total_output_neurons):
                sum += o_gradient[k][0] * w2T[j][k]

            rh2_gradient.append(d_relu2[j][0] * sum)

        return np.array(rh2_gradient).reshape(-1, 1)

    def get_rh1_gradient(self, d_relu1, rh2_gradient):
        rh1_gradient = []
        w1T = np.transpose(self.weights_list[1])
        for j in range(self.total_neurons_per_hidden_layer):
            sum = 0
            for k in range(self.total_neurons_per_hidden_layer):
                sum += rh2_gradient[k][0] * w1T[j][k]

            rh1_gradient.append(d_relu1[j][0] * sum)

        return np.array(rh1_gradient).reshape(-1, 1)

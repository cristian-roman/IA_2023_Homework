import numpy as np

from instance import Instance

from neuralNetworkUtils import NeuralNetworkUtils as NNU


class TrainingNeuralNetwork:
    number_of_input_neurons = 7
    number_of_hidden_layers = 2
    number_of_output_neurons = 3
    learning_rate = 0.045
    max_number_of_epochs = 1000

    def __init__(self, instances: np.array(Instance)):
        self.number_of_neurons_per_hidden_layer = int(
            2 / 3 * self.number_of_input_neurons + self.number_of_output_neurons)
        self.instances = instances
        self.weights_list = []
        self.biases_list = []
        self.initialize_weights_and_biases()

    def initialize_weights_and_biases(self):
        np.random.seed(14)
        first_hidden_layer_weights = NNU.he_initialization(self.number_of_input_neurons,
                                                           self.number_of_neurons_per_hidden_layer)
        first_hidden_layer_biases = np.random.normal(0, 1, size=(self.number_of_neurons_per_hidden_layer, 1))

        second_hidden_layer_weights = NNU.he_initialization(self.number_of_neurons_per_hidden_layer,
                                                            self.number_of_neurons_per_hidden_layer)
        second_hidden_layer_biases = np.random.normal(0, 1, size=(self.number_of_neurons_per_hidden_layer, 1))

        output_layer_weights = NNU.he_initialization(self.number_of_neurons_per_hidden_layer,
                                                     self.number_of_output_neurons)
        output_layer_biases = np.random.normal(0, 1, size=(self.number_of_output_neurons, 1))

        self.weights_list.append(first_hidden_layer_weights)
        self.weights_list.append(second_hidden_layer_weights)
        self.weights_list.append(output_layer_weights)

        self.biases_list.append(first_hidden_layer_biases)
        self.biases_list.append(second_hidden_layer_biases)
        self.biases_list.append(output_layer_biases)

    def train(self):
        for epoch in range(self.max_number_of_epochs):
            for instance in self.instances:
                neurons = NNU.propagate_forward(instance[0].attributes, self.weights_list, self.biases_list)
                self.back_propagate(instance[0], neurons)

            if epoch % 100 == 0:
                print("The epoch: " + str(epoch) + " is done")
                print("Train accuracy: " + str(self.get_accuracy(self.instances)))

    def back_propagate(self, instance, neurons):

        # critical line
        second_to_exit_delta = self.get_delta_second_to_exit(instance, neurons)

        other_deltas = self.get_delta_sub_weights(instance, neurons, second_to_exit_delta[2])

        # critical line
        self.update_weights_and_biases(other_deltas, second_to_exit_delta)

    def get_delta_sub_weights(self, instance, neurons, last_computed_cost_derivative):

        number_of_left_weights = self.number_of_hidden_layers + 1 - 1

        deltas = []

        for i in range(number_of_left_weights, 0, -1):
            last_used_weights = self.weights_list[i]
            current_relu_output = neurons[i * 2 - 1]
            current_weights = self.weights_list[i - 1]

            if i == 1:
                current_raw_output = instance.attributes
            else:
                current_raw_output = neurons[i * 2 - 3]

            last_output_derivative_to_relu = NNU.raw_output_derivative_to_reLU(last_used_weights)
            relu_derivative_to_next_output = NNU.reLU_derivative_to_next_output(current_relu_output)
            next_input_derivative_to_weights = NNU.raw_output_derivative_to_weights(current_weights, current_raw_output)
            next_input_derivative_to_bias = NNU.raw_output_derivative_to_biases()

            if i == 2:
                temp1 = np.dot(last_output_derivative_to_relu, last_computed_cost_derivative)
                temp2 = np.multiply(relu_derivative_to_next_output, temp1.reshape(1, -1))
            else:
                temp1 = np.dot(last_output_derivative_to_relu, last_computed_cost_derivative.reshape(-1,1))
                temp2 = np.multiply(relu_derivative_to_next_output, temp1.reshape(1, -1))

            delta_sub_weights = np.multiply(temp2, next_input_derivative_to_weights)
            if delta_sub_weights.shape[0] != self.weights_list[i - 1].shape[0] or delta_sub_weights.shape[1] != self.weights_list[i - 1].shape[1]:
                delta_sub_weights = delta_sub_weights.reshape(self.weights_list[i-1].shape[0], self.weights_list[i-1].shape[1])

            delta_sub_bias = np.multiply(temp2, next_input_derivative_to_bias)
            if delta_sub_bias.shape[0] != self.biases_list[i - 1].shape[0] or delta_sub_bias.shape[1] != self.biases_list[i - 1].shape[1]:
                delta_sub_bias = delta_sub_bias.reshape(self.biases_list[i-1].shape[0], self.biases_list[i-1].shape[1])

            deltas.append((delta_sub_weights, delta_sub_bias))

            last_computed_cost_derivative = temp2

        return deltas

    def get_delta_second_to_exit(self, instance, neurons):
        expected_output = instance.expected_output
        second_to_exit_softmax_output = neurons[-1]
        second_to_exit_output = neurons[-2]
        second_to_exit_weights = self.weights_list[-1]
        first_to_second_reLU_output = neurons[-3]

        error_to_softmax = NNU.cross_validation_error_derivative_to_softmax(expected_output,
                                                                            second_to_exit_softmax_output)
        softmax_derivative_to_exit_output = NNU.softmax_derivative_to_exit_output(second_to_exit_output)

        exit_output_derivative_to_weights = NNU.raw_output_derivative_to_weights(second_to_exit_weights,
                                                                                 first_to_second_reLU_output)
        exit_output_derivative_to_biases = NNU.raw_output_derivative_to_biases()

        temp1 = np.multiply(error_to_softmax, softmax_derivative_to_exit_output).reshape(-1, 1)

        delta_second_to_exit_weights = np.multiply(temp1, exit_output_derivative_to_weights)
        delta_second_to_exit_biases = np.multiply(temp1, exit_output_derivative_to_biases)

        return delta_second_to_exit_weights, delta_second_to_exit_biases, temp1

    def update_weights_and_biases(self, other_deltas, second_to_exit_delta):

        # update first weights and biases backward

        self.weights_list[self.number_of_hidden_layers] = self.weights_list[
                                                              self.number_of_hidden_layers] - self.learning_rate * \
                                                          second_to_exit_delta[0]
        self.biases_list[self.number_of_hidden_layers] = self.biases_list[
                                                             self.number_of_hidden_layers] - self.learning_rate * \
                                                         second_to_exit_delta[1]

        # update other weights and biases backward
        for i in range(len(other_deltas)):
            weight_index = self.number_of_hidden_layers - i - 1
            self.weights_list[weight_index] = self.weights_list[weight_index] - self.learning_rate * other_deltas[i][0]
            self.biases_list[weight_index] = self.biases_list[weight_index] - self.learning_rate * other_deltas[i][1]

    def get_accuracy(self, instances):
        correct_predictions = 0
        for instance in instances:
            neurons = NNU.propagate_forward(instance[0].attributes, self.weights_list, self.biases_list)
            output = neurons[-1]
            label = -1
            for i in range(len(output)):
                if output[i] == max(output):
                    label = i
                    break
            if label == instance[0].raw_output:
                correct_predictions += 1

        return correct_predictions / len(instances) * 100

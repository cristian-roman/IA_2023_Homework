import numpy as np


class NeuralNetworkUtils:
    @staticmethod
    def propagate_forward(instance_input: np.array(np.float32), weights_list: list[np.array(np.float32)],
                          biases_list: list[np.array(np.float32)]):

        # first propagation
        weights = weights_list[0]
        initial_to_first_output = np.dot(weights, instance_input) + biases_list[0]
        initial_to_first_reLU_output = NeuralNetworkUtils.__reLU(initial_to_first_output)

        # second propagation
        weights = weights_list[1]
        first_to_second_output = np.dot(weights, initial_to_first_reLU_output) + biases_list[1]
        first_to_second_reLU_output = NeuralNetworkUtils.__reLU(first_to_second_output)

        # output propagation
        weights = weights_list[2]
        second_to_exit_output = np.dot(weights, first_to_second_reLU_output) + biases_list[2]
        second_to_exit_softmax_output = NeuralNetworkUtils.__softmax(second_to_exit_output)

        return (initial_to_first_output, initial_to_first_reLU_output,
                first_to_second_output, first_to_second_reLU_output,
                second_to_exit_output, second_to_exit_softmax_output)

    @staticmethod
    def __reLU(raw_output):  # input: number, output: number
        reLU_output = []
        for raw_output_value in raw_output:
            if raw_output_value > 0:
                reLU_output.append(raw_output_value[0])
            else:
                reLU_output.append(0)
        return np.array(reLU_output).reshape(-1, 1)

    @staticmethod
    def __softmax(output_layer) -> np.array(np.float32):  # input: vector, output:vector
        new_output_layer = []
        sum = 0
        for raw_output in output_layer:
            sum += np.exp(raw_output)

        for raw_output in output_layer:
            new_output_layer.append(np.exp(raw_output) / sum)

        return np.array(new_output_layer).reshape(-1, 1)

    # @staticmethod
    # def __cross_validation_error(instance_output_distribution, propagated_output_distribution):
    #     error = 0
    #     for i in range(len(instance_output_distribution)):
    #         error += instance_output_distribution[i] * np.log(propagated_output_distribution[i])
    #     return error * / len(instance_output_distribution)

    @staticmethod
    def cross_validation_error_derivative_to_softmax(expected_output, second_to_exit_softmax_layer):
        derivatives = (
            NeuralNetworkUtils.__cross_validation_error_partial_derivative_to_softmax_value(expected_output[0],
                                                                                            second_to_exit_softmax_layer[
                                                                                                0]),
            NeuralNetworkUtils.__cross_validation_error_partial_derivative_to_softmax_value(expected_output[1],
                                                                                            second_to_exit_softmax_layer[
                                                                                                1]),
            NeuralNetworkUtils.__cross_validation_error_partial_derivative_to_softmax_value(expected_output[2],
                                                                                            second_to_exit_softmax_layer[
                                                                                                2]))

        return np.array(derivatives).reshape(1, 3)

    @staticmethod
    def __cross_validation_error_partial_derivative_to_softmax_value(partial_expected_output_value,
                                                                     partial_softmax_output):
        return partial_expected_output_value / (3 * partial_softmax_output)

    @staticmethod
    def softmax_derivative_to_exit_output(second_to_exit_output):
        derivative = (NeuralNetworkUtils.__softmax_partial_derivative_to_raw_output(second_to_exit_output[0]),
                      NeuralNetworkUtils.__softmax_partial_derivative_to_raw_output(second_to_exit_output[1]),
                      NeuralNetworkUtils.__softmax_partial_derivative_to_raw_output(second_to_exit_output[2]))

        return np.array(derivative).reshape(1, 3)

    @staticmethod
    def __softmax_partial_derivative_to_raw_output(specific_raw_output):
        # specific point
        return specific_raw_output * (1 - specific_raw_output)

    @staticmethod
    def raw_output_derivative_to_weights(weights, raw_output):
        derivative = []
        for i in range(len(weights)):
            derivative.append(NeuralNetworkUtils.__raw_output_partial_derivative_to_weight_row(raw_output))

        return np.array(derivative).reshape(len(weights), len(raw_output))

    @staticmethod
    def __raw_output_partial_derivative_to_weight_row(raw_output):
        return np.transpose(raw_output)

    @staticmethod
    def raw_output_derivative_to_biases():
        return np.array(1).reshape(1, 1)

    @staticmethod
    def raw_output_derivative_to_reLU(weights):
        return np.transpose(weights)

    @staticmethod
    def reLU_derivative_to_next_output(current_ReLU_output):  # next: backwards
        derivative = []
        for i in range(len(current_ReLU_output)):
            derivative.append(NeuralNetworkUtils.__reLU_partial_derivative_to_previous_neuron(current_ReLU_output[i]))

        return np.array(derivative).reshape(1, len(current_ReLU_output))

    @staticmethod
    def __reLU_partial_derivative_to_previous_neuron(reLU_neuron_value):
        if reLU_neuron_value > 0:
            return 1
        else:
            return 0

    @staticmethod
    def he_initialization(number_of_neurons_previous_layer, number_of_neurons_current_layer):
        variance = 2 / number_of_neurons_previous_layer
        standard_deviation = np.sqrt(variance)
        weights = np.random.normal(0, standard_deviation,
                                   (number_of_neurons_current_layer, number_of_neurons_previous_layer))
        return weights

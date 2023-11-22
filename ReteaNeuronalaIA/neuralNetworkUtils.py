import numpy as np


class NeuralNetworkUtils:

    @staticmethod
    def he_initialization(total_neurons_from_layer: int, total_neurons_to_layer: int):
        variance = 2 / total_neurons_from_layer
        standard_deviation = np.sqrt(variance)
        weights = np.random.normal(0, standard_deviation, (total_neurons_to_layer, total_neurons_from_layer))
        return weights

    @staticmethod
    def __reLU(x_vector):
        reLU_output = []
        for x_value in x_vector:
            if x_value > 0:
                reLU_output.append(x_value[0])
            else:
                reLU_output.append(0)
        return np.array(reLU_output).reshape(-1, 1)

    @staticmethod
    def __softmax(x_vector):
        softmax_output = []
        sum = 0
        for x_value in x_vector:
            sum += np.exp(x_value)

        for x_value in x_vector:
            softmax_output.append(np.exp(x_value) / sum)

        return np.array(softmax_output).reshape(-1, 1)

    @staticmethod
    def propagate_forward(instance_input, weights_list, biases_list):
        # first propagation
        h1 = np.dot(weights_list[0], instance_input) + biases_list[0]
        rh1 = NeuralNetworkUtils.__reLU(h1)

        # second propagation
        h2 = np.dot(weights_list[1], rh1) + biases_list[1]
        rh2 = NeuralNetworkUtils.__reLU(h2)

        # output propagation
        o = np.dot(weights_list[2], rh2) + biases_list[2]
        so = NeuralNetworkUtils.__softmax(o)

        return h1, rh1, h2, rh2, o, so

    @staticmethod
    def d_softmax(softmax_values):
        arr = []
        for v in softmax_values:
            arr.append(v * (1 - v))

        return np.array(arr).reshape(-1, 1)

    @staticmethod
    def cost_gradient(expected_output, actual_output):
        return expected_output - actual_output

    @staticmethod
    def d_reLU(x_vector):
        d_reLU_output = []
        for x_value in x_vector:
            if x_value > 0:
                d_reLU_output.append(1)
            else:
                d_reLU_output.append(0)
        return np.array(d_reLU_output).reshape(-1, 1)

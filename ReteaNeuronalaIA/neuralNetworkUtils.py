import numpy as np
from instance import Instance


class NeuralNetworkUtils:
    @staticmethod
    def propagate_forward(instance: Instance, weights_list: list[np.array(np.float32)]):
        # Add the bias to the instance
        input_with_bias = np.append(instance.attributes, 1)  # bias added on the last position

        # first propagation
        first_hidden_layer = []
        weights = weights_list[0]

        for weight in weights:
            raw_output = np.dot(input_with_bias, weight)
            output = NeuralNetworkUtils.__reLU(raw_output)
            first_hidden_layer.append(output)

        # second propagation
        first_hidden_layer.append(1)  # bias added on the last position
        second_hidden_layer = []
        weights = weights_list[1]

        for weight in weights:
            raw_output = np.dot(first_hidden_layer, weight)
            output = NeuralNetworkUtils.__reLU(raw_output)
            second_hidden_layer.append(output)

        # output propagation
        second_hidden_layer.append(1)  # bias added on the last position
        output_layer = []
        weights = weights_list[2]

        for weight in weights:
            raw_output = np.dot(second_hidden_layer, weight)
            output_layer.append(raw_output)

        output_layer = NeuralNetworkUtils.__softmax(output_layer)

        return output_layer

    @staticmethod
    def __reLU(x):
        return max(0, x)

    @staticmethod
    def __softmax(output_layer):
        new_output_layer = []
        sum = 0
        for raw_output in output_layer:
            sum += np.exp(raw_output)

        for raw_output in output_layer:
            new_output_layer.append(np.exp(raw_output) / sum)

        return new_output_layer

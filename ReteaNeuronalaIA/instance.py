import numpy as np
import copy


class Instance:
    number_of_classifications = 3
    number_of_attributes = 7

    def __init__(self, attributes: np.array(np.float32), expected_output: int):
        self.attributes = Instance.__normalize_attributes(attributes)
        self.raw_output = expected_output

        self.attributes = np.array(self.attributes).reshape(self.number_of_attributes, 1)
        self.expected_output = self.__model_output_vector(expected_output)

    def __str__(self):
        return f'attributes: {self.attributes}, expected_output: {self.expected_output}'

    def __model_output_vector(self, expected_output):
        output_vector = []
        for i in range(1, self.number_of_classifications + 1):
            if i == expected_output:
                output_vector.append(1)
            else:
                output_vector.append(0)
        return np.array(output_vector).reshape(-1, 1)

    @staticmethod
    def __normalize_attributes(attributes):
        normalized_attributes = []
        for attribute in attributes:
            normalized_attributes.append(attribute/15)

        return np.array(normalized_attributes).reshape(-1, 1)

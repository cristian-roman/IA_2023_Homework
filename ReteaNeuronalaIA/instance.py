import numpy as np
import copy


class Instance:
    number_of_classifications = 3

    def __init__(self, attributes: np.array(np.float32), expected_output: int):
        self.attributes = copy.deepcopy(attributes)
        output_vector = []
        for i in range(self.number_of_classifications):
            if i == expected_output:
                output_vector.append(1)
            else:
                output_vector.append(0)
        self.expected_output = np.array(output_vector).reshape(-1, 1)

    def __str__(self):
        return f'attributes: {self.attributes}, expected_output: {self.expected_output}'

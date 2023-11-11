import numpy as np
import copy


class Instance:
    def __init__(self, attributes: np.array(np.float32), expected_output: int):
        self.attributes = copy.deepcopy(attributes)
        self.expected_output = expected_output

    def __str__(self):
        return f'attributes: {self.attributes}, expected_output: {self.expected_output}'

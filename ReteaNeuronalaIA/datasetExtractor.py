import numpy as np

from instance import Instance


class DataSetExtractor:
    def __init(self):
        pass

    @staticmethod
    def extract() -> np.array(Instance):
        file_path = 'seeds_dataset.txt'
        instances = []
        with open(file_path, 'r') as file:
            for line in file:
                values = line.strip().split('\t')

                # Extract the attributes (first 7 values) and the expected output (last value)
                attributes = list(map(np.float32, values[:-1]))
                expected_output = int(values[-1])

                instances.append(Instance(attributes, expected_output))

        return np.array(instances).reshape(-1, 1)


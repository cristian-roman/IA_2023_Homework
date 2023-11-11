import numpy as np

from datasetExtractor import DataSetExtractor

import trainingNeuralNetwork as tnn

if __name__ == '__main__':
    instances = DataSetExtractor.extract()
    np.random.shuffle(instances)

    # Split the dataset into training and testing sets
    training_ratio = 0.8  # 80% of the dataset will be used for training

    total_instances = len(instances)
    training_instances = int(total_instances * training_ratio)
    testing_instances = total_instances - training_instances

    training_set = instances[:training_instances]
    testing_set = instances[training_instances:]

    trainingNeuralNetwork = tnn.TrainingNeuralNetwork(training_set)
    print(trainingNeuralNetwork.propagate_forward(testing_set[0][0]))

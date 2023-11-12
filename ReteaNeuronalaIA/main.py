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
    trainingNeuralNetwork.train()

    # testing
    correct_predictions = 0
    for instance in testing_set:
        neurons = tnn.NeuralNetworkUtils.propagate_forward(instance[0].attributes, trainingNeuralNetwork.weights_list)
        output = neurons[-1]
        label = -1
        for i in range(len(output)):
            if output[i] == max(output):
                label = i
                break
        if label == instance[0].raw_output:
            correct_predictions += 1

    print(f'Accuracy: {correct_predictions / testing_instances * 100}%')

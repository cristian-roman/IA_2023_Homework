import numpy as np

from datasetExtractor import DataSetExtractor

from trainingNeuralNetwork import TrainingNeuralNetwork
from neuralNetworkUtils import NeuralNetworkUtils as NNU

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

    trainingNeuralNetwork = TrainingNeuralNetwork(training_set)
    trainingNeuralNetwork.train()

    # Test the neural network
    correct_predictions = 0
    for instance in testing_set:
        neurons = NNU.propagate_forward(instance[0].attributes, trainingNeuralNetwork.weights_list,
                                        trainingNeuralNetwork.biases_list)

        if np.argmax(neurons[5]) + 1 == instance[0].raw_output:
            correct_predictions += 1

    print(f'Accuracy: {correct_predictions / testing_instances * 100}%')
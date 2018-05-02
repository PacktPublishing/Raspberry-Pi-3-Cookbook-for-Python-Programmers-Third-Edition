import numpy as np
import neurolab as nl

# Input file
in_file = 'words.data'

# Number of datapoints to load from the input file
num_of_datapoints = 20

# Distinct characters
original_labels = 'omandig'

# Number of distinct characters
num_of_charect = len(original_labels)

# Training and testing parameters
train_param = int(0.9 * num_of_datapoints)
test_param = num_of_datapoints - train_param

# Define dataset extraction parameters 
s_index = 6
e_index = -1

# Creating the dataset
information = []
labels = []
with open(in_file, 'r') as f:
    for line in f.readlines():
        # Split the line tabwise
        list_of_values = line.split('\t')

        # If the label is not in our ground truth labels, skip it
        if list_of_values[1] not in original_labels:
            continue

        # Extract the label and append it to the main list
        label = np.zeros((num_of_charect , 1))
        label[original_labels.index(list_of_values[1])] = 1
        labels.append(label)

        # Extract the character vector and append it to the main list
        extract_char = np.array([float(x) for x in list_of_values[s_index:e_index]])
        information.append(extract_char)

        # Exit the loop once the required dataset has been loaded
        if len(information) >= num_of_datapoints:
            break

# Convert information and labels to numpy arrays
information = np.array(information)
labels = np.array(labels).reshape(num_of_datapoints, num_of_charect)

# Extract number of dimensions
num_dimension = len(information[0])

# Create and train neural network
neural_net = nl.net.newff([[0, 1] for _ in range(len(information[0]))], [128, 16, num_of_charect])
neural_net.trainf = nl.train.train_gd
error = neural_net.train(information[:train_param,:], labels[:train_param,:], epochs=10000, show=100, goal=0.01)

# Predict the output for test inputs 
p_output = neural_net.sim(information[train_param:, :])
print "\nTesting on unknown data:"
for i in range(test_param):
    print "\nOriginal:", original_labels[np.argmax(labels[i])]
    print "Predicted:", original_labels[np.argmax(p_output[i])]


from sklearn import cross_validation
from sklearn.naive_bayes import GaussianNB
import numpy as np
import matplotlib.pyplot as plt

in_file = 'data_multivar.txt'
a = []
b = []
with open(in_file, 'r') as f:
	for line in f.readlines():
		data = [float(x) for x in line.split(',')]
		a.append(data[:-1])
		b.append(data[-1])
a = np.array(a)
b = np.array(b)

a_training, a_testing, b_training, b_testing = cross_validation.train_test_split(a, b,
test_size=0.25, random_state=5)
classification_gaussiannb_new = GaussianNB()
classification_gaussiannb_new.fit(a_training, b_training)


b_test_pred = classification_gaussiannb_new.predict(a_testing)

correctness = 100.0 * (b_testing == b_test_pred).sum() / a_testing.shape[0]
print "correctness of the classification =", round(correctness, 2), "%"

def plot_classification(classification_gaussiannb_new, a_testing , b_testing):

	a_min, a_max = min(a_testing[:, 0]) - 1.0, max(a_testing[:, 0]) + 1.0
	b_min, b_max = min(a_testing[:, 1]) - 1.0, max(a_testing[:, 1]) + 1.0

	step_size = 0.01

	a_values, b_values = np.meshgrid(np.arange(a_min, a_max, step_size), np.arange(b_min, b_max, step_size))


	mesh_output = classification_gaussiannb_new.predict(np.c_[a_values.ravel(), b_values.ravel()])

	mesh_output = mesh_output.reshape(a_values.shape)

	plt.figure()

	plt.pcolormesh(a_values, b_values, mesh_output, cmap=plt.cm.gray)

	plt.scatter(a_testing[:, 0], a_testing[:, 1], c=b_testing , s=80, edgecolors='black', linewidth=1,cmap=plt.cm.Paired)
	# specify the boundaries of the figure
	plt.xlim(a_values.min(), a_values.max())
	plt.ylim(b_values.min(), b_values.max())
	# specify the ticks on the X and Y axes
	plt.xticks((np.arange(int(min(a_testing[:, 0])-1), int(max(a_testing[:, 0])+1), 1.0)))
	plt.yticks((np.arange(int(min(a_testing[:, 1])-1), int(max(a_testing[:, 1])+1), 1.0)))
	plt.show()

plot_classification(classification_gaussiannb_new, a_testing, b_testing)

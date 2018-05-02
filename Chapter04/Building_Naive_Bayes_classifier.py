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

classification_gaussiannb = GaussianNB()
classification_gaussiannb.fit(a, b)
b_pred = classification_gaussiannb.predict(a)

correctness = 100.0 * (b == b_pred).sum() / a.shape[0]
print "correctness of the classification =", round(correctness, 2), "%"



def plot_classification(classification_gaussiannb, a , b):

	a_min, a_max = min(a[:, 0]) - 1.0, max(a[:, 0]) + 1.0
	b_min, b_max = min(a[:, 1]) - 1.0, max(a[:, 1]) + 1.0

	step_size = 0.01

	a_values, b_values = np.meshgrid(np.arange(a_min, a_max, step_size), np.arange(b_min, b_max, step_size))

	mesh_output1 = classification_gaussiannb.predict(np.c_[a_values.ravel(), b_values.ravel()])

	mesh_output2 = mesh_output1.reshape(a_values.shape)

	plt.figure()

	plt.pcolormesh(a_values, b_values, mesh_output2, cmap=plt.cm.gray)

	plt.scatter(a[:, 0], a[:, 1], c=b , s=80, edgecolors='black', linewidth=1,cmap=plt.cm.Paired)
	# specify the boundaries of the figure
	plt.xlim(a_values.min(), a_values.max())
	plt.ylim(b_values.min(), b_values.max())
	# specify the ticks on the X and Y axes
	plt.xticks((np.arange(int(min(a[:, 0])-1), int(max(a[:, 0])+1), 1.0)))
	plt.yticks((np.arange(int(min(a[:, 1])-1), int(max(a[:, 1])+1), 1.0)))
	plt.show()

plot_classification(classification_gaussiannb, a, b)



from sklearn import cross_validation
from sklearn.naive_bayes import GaussianNB
import numpy as np

in_file = 'cross_validation_multivar.txt'
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

num_of_validations = 5
accuracy = cross_validation.cross_val_score(classification_gaussiannb, a, b, scoring='accuracy', cv=num_of_validations)
print "Accuracy: " + str(round(100* accuracy.mean(), 2)) + "%"
f1 = cross_validation.cross_val_score(classification_gaussiannb, a, b, scoring='f1_weighted', cv=num_of_validations)
print "f1: " + str(round(100*f1.mean(), 2)) + "%" 
precision = cross_validation.cross_val_score(classification_gaussiannb,a, b, scoring='precision_weighted', cv=num_of_validations)
print "Precision: " + str(round(100*precision.mean(), 2)) + "%"
recall = cross_validation.cross_val_score(classification_gaussiannb, a, b, scoring='recall_weighted', cv=num_of_validations)
print "Recall: " + str(round(100*recall.mean(), 2)) + "%"

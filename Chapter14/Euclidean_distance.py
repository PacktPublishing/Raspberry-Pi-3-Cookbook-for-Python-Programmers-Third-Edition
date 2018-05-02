import json
import numpy as np

def euclidean_dist_score(dataset, FirstUser, SecondUser):
 	if FirstUser not in dataset:
		raiseTypeError('User ' + FirstUser + ' not present in the dataset')
	if SecondUser not in dataset:
		raiseTypeError('User ' + SecondUser + ' not present in the dataset')

	# Movies rated by both FirstUser and SecondUser
	Both_User_rated = {}
	for element in dataset[FirstUser]:
		if element in dataset[SecondUser]:
			Both_User_rated[element] = 1

	# Score 0 indicate no common movies
	if len(Both_User_rated) == 0:
	    return 0

	SquareDifference = []
	for element in dataset[FirstUser]:
	     if element in dataset[SecondUser]:
	        SquareDifference.append(np.square(dataset[FirstUser][element] - dataset[SecondUser][element]))	

	return 1 / (1 + np.sqrt(np.sum(SquareDifference)))

if __name__=='__main__':
	data_file = 'movie_rating.json'
	with open(data_file, 'r') as m:
	  dataset = json.loads(m.read())

	FirstUser = 'Steven Ferndndes'
	SecondUser = 'Ramesh Nayak'
	print "\nEuclidean score:"
	print euclidean_dist_score(dataset, FirstUser, SecondUser)





import json
import numpy as np

# Returns the Pearson correlation score between user1 and user2
def pearson_dist_score(dataset, FirstUser, SecondUser):
	if FirstUser not in dataset:
	   raise TypeError('User ' + FirstUser + ' not present in the dataset')
	if SecondUser not in dataset:
	   raise TypeError('User ' + SecondUser + ' not present in the dataset')

	# Movies rated by both FirstUser and SecondUser
	both_User_rated = {}
	for element in dataset[FirstUser]:
	   if element in dataset[SecondUser]:
	      both_User_rated[element] = 1

	rating_number = len(both_User_rated)

	# Score 0 indicate no common movies
	if rating_number == 0:
	   return 0

	# Calculate the sum of ratings of all the common preferences
	FirstUser_sum = np.sum([dataset[FirstUser][element] for element in both_User_rated])
	SecondUser_sum = np.sum([dataset[SecondUser][element] for element in both_User_rated])

	# Calculate the sum of squared ratings of all the common preferences
	FirstUser_squared_sum = np.sum([np.square(dataset[FirstUser][element]) for element in both_User_rated])
	SecondUser_squared_sum = np.sum([np.square(dataset[SecondUser][element]) for element in both_User_rated])

	# Calculate the sum of products of the common ratings
	sum_product = np.sum([dataset[FirstUser][element] * dataset[SecondUser][element] for element in both_User_rated])

	# Pearson correlation calculation

	PSxy = sum_product - (FirstUser_sum * SecondUser_sum / rating_number)
	PSxx = FirstUser_squared_sum - np.square(FirstUser_sum) / rating_number
	PSyy = SecondUser_squared_sum - np.square(SecondUser_sum) / rating_number

	if PSxx * PSyy == 0:
	  return 0

	return PSxy / np.sqrt(PSxx * PSyy)

if __name__=='__main__':
	data_file = 'movie_rating.json'
	with open(data_file, 'r') as m:
	  	dataset = json.loads(m.read())
	  	FirstUser = 'Steven Ferndndes'
		SecondUser = 'Ramesh Nayak'
		print "\nPearson score:"
		print pearson_dist_score(dataset, FirstUser, SecondUser)




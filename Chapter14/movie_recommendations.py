import json
import numpy as np

def pearson_dist_score(dataset, user, s):
	if user not in dataset:
	   raise TypeError('User ' + user + ' not present in the dataset')
	if s not in dataset:
	   raise TypeError('User ' + s + ' not present in the dataset')
    
	# Movies rated by both FirstUser and SecondUser
	both_User_rated = {}
	for element in dataset[user]:
	   if element in dataset[s]:
	      both_User_rated[element] = 1

	rating_number = len(both_User_rated)

	# Score 0 indicate no common movies
	if rating_number == 0:
	   return 0

	# Calculate the sum of ratings of all the common preferences
	user_sum = np.sum([dataset[user][element] for element in both_User_rated])
	s_sum = np.sum([dataset[s][element] for element in both_User_rated])

	# Calculate the sum of squared ratings of all the common preferences
	user_squared_sum = np.sum([np.square(dataset[user][element]) for element in both_User_rated])
	s_squared_sum = np.sum([np.square(dataset[s][element]) for element in both_User_rated])

	# Calculate the sum of products of the common ratings
	sum_product = np.sum([dataset[user][element] * dataset[s][element] for element in both_User_rated])

	# Pearson correlation calculation

	PSxy = sum_product - (user_sum * s_sum / rating_number)
	PSxx = user_squared_sum - np.square(user_sum) / rating_number
	PSyy = s_squared_sum - np.square(s_sum) / rating_number

	
	if PSxx * PSyy == 0:
	  return 0

	return PSxy / np.sqrt(PSxx * PSyy)

# Generate recommendations for a given user
def movie_recommendations(dataset , user):
    if user not in dataset:
        raise TypeError('User ' + user + ' not present in the dataset')

    scores_sum = {}
    sum_similarity = {}

    for s in [a for a in dataset if a != user]:
        score_similarity = pearson_dist_score(dataset , user, s)

        if score_similarity <= 0:
            continue
           
        for element in [a for a in dataset[s] if a not in dataset[user] or dataset[user][a] == 0]:
            
            scores_sum.update({element: dataset[s][element] * score_similarity})
            sum_similarity.update({element: score_similarity})

    if len(scores_sum) == 0:
        return ['No recommendations possible']

    # Create the normalized list
    movie_ranking = np.array([[total/sum_similarity[element], element] 
            for element, total in scores_sum.items()])

    # Sort in decreasing order based on the first column
    movie_ranking = movie_ranking[np.argsort(movie_ranking[:, 0])[::-1]]

    # Extract the recommended movies
    recommendies = [movie for _,movie in movie_ranking]

    return  recommendies
 
if __name__=='__main__':
    data_file = 'movie_rating.json'

    with open(data_file, 'r') as f:
        dataset = json.loads(f.read())

    user = 'Steven Ferndndes'
    print "\nRecommendations for " + user + ":"
    movie = movie_recommendations(dataset, user) 
    for i, movies in enumerate(movie):
        print str(i+1) + '. ' + movies

    user = 'Ramesh Nayak' 
    print "\nRecommendations for " + user + ":"
    movie = movie_recommendations(dataset, user) 
    for i, movies in enumerate(movie):
        print str(i+1) + '. ' + movies

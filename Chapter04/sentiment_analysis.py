import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews

def collect_features(word_list):
        	word = []
                return dict ([(word, True) for word in word_list])


if __name__=='__main__':
			plus_filenum = movie_reviews.fileids('pos')
			minus_filenum = movie_reviews.fileids('neg')

			feature_pluspts = [(collect_features(movie_reviews.words(fileids=[f])),
				'Positive') for f in plus_filenum]
    			feature_minuspts = [(collect_features(movie_reviews.words(fileids=[f])),
				'Negative') for f in minus_filenum]

    			threshold_fact = 0.8
    			threshold_pluspts = int(threshold_fact * len(feature_pluspts))
    			threshold_minuspts = int(threshold_fact * len(feature_minuspts))

    			feature_training = feature_pluspts[:threshold_pluspts] + feature_minuspts[:threshold_minuspts]
    			feature_testing = feature_pluspts[threshold_pluspts:] + feature_minuspts[threshold_minuspts:] 
    			print "\nNumber of training datapoints:", len(feature_training)
    			print "Number of test datapoints:", len(feature_testing)

		    	# Train a Naive Bayes classifiers
		    	classifiers = NaiveBayesClassifier.train(feature_training)
		    	print "\nAccuracy of the classifiers:", nltk.classify.util.accuracy(classifiers,feature_testing)

		    	print "\nTop 10 most informative words:"
		    	for item in classifiers.most_informative_features()[:10]:print item[0]

		    	# Sample input reviews
		    	in_reviews = [
			"The Movie was amazing",
			"the movie was dull. I would never recommend it to anyone.",
			"The cinematography is pretty great in the movie",
			"The direction was horrible and the story was all over the place"
		    	]

		    	print "\nPredictions:"
		    	for review in in_reviews:
				print "\nReview:", review
			probdist = classifiers.prob_classify(collect_features(review.split()))
			predict_sentiment = probdist.max()

			print "Predicted sentiment:", predict_sentiment
			print "Probability:", round(probdist.prob(predict_sentiment), 2)

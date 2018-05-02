from sklearn.datasets import fetch_20newsgroups

category_mapping = {'misc.forsale': 'Sellings', 'rec.motorcycles': 'Motorbikes',
        'rec.sport.baseball': 'Baseball', 'sci.crypt': 'Cryptography',
        'sci.space': 'OuterSpace'}

training_content = fetch_20newsgroups(subset='train',
		categories=category_mapping.keys(), shuffle=True, random_state=7)

# Feature extraction
from sklearn.feature_extraction.text import CountVectorizer

vectorizing = CountVectorizer()
train_counts = vectorizing.fit_transform(training_content.data)
print "\nDimensions of training data:", train_counts.shape

# Training a classifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer

input_content = [
    "The curveballs of right handed pitchers tend to curve to the left",
    "Caesar cipher is an ancient form of encryption",
    "This two-wheeler is really good on slippery roads"
]

# tf-idf transformer
tfidf_transformer = TfidfTransformer()
train_tfidf = tfidf_transformer.fit_transform(train_counts)

# Multinomial Naive Bayes classifier
classifier = MultinomialNB().fit(train_tfidf, training_content.target)

input_counts = vectorizing.transform(input_content)

input_tfidf = tfidf_transformer.transform(input_counts)

# Predict the output categories
categories_prediction = classifier.predict(input_tfidf)

# Print the outputs
for sentence, category in zip(input_content, categories_prediction):
    print '\nInput:', sentence, '\nPredicted category:', \
            category_mapping[training_content.target_names[category]]

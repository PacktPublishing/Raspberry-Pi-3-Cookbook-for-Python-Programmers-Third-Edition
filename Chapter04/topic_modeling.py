

from nltk.tokenize import RegexpTokenizer 
from nltk.stem.snowball import SnowballStemmer
from gensim import models, corpora
from nltk.corpus import stopwords

# Load input words
def load_words(in_file):
    element = []
    with open(in_file, 'r') as f:
        for line in f.readlines():
            element.append(line[:-1])
    return element

# Class to preprocedure of text
class Preprocedure(object):
    # Initialize various operators
    def __init__(self):
        # Create a regular expression tokenizer
        self.tokenizer = RegexpTokenizer(r'\w+')

        # get the list of stop words
        self.english_stop_words= stopwords.words('english')

        # Create a Snowball stemmer
        self.snowball_stemmer = SnowballStemmer('english')

    # Tokenizing, stop word removal, and stemming
    def procedure(self, in_data):
        # Tokenize the string

        token = self.tokenizer.tokenize(in_data.lower())

        # Remove the stop words
        tokenized_stopwords = [x for x in token if not x in self.english_stop_words]

        # Perform stemming on the tokens
        token_stemming = [self.snowball_stemmer.stem(x) for x in tokenized_stopwords]

        return token_stemming

if __name__=='__main__':
    # File containing linewise input data
    in_file = 'data_topic_modeling.txt'
    # Load words
    element = load_words(in_file)

    # Create a preprocedure object
    preprocedure = Preprocedure()

    # Create a list for processed documents
    processed_tokens = [preprocedure.procedure(x) for x in element]

    # Create a dictionary based on the tokenized documents
    dict_tokens = corpora.Dictionary(processed_tokens)

    corpus = [dict_tokens.doc2bow(text) for text in processed_tokens]

    # Generate the LDA model based on the corpus we just created
    num_of_topics = 2
    num_of_words = 4
    ldamodel = models.ldamodel.LdaModel(corpus,
            num_topics=num_of_topics, id2word=dict_tokens, passes=25)

    print "Most contributing words to the topics:"
    for item in ldamodel.print_topics(num_topics=num_of_topics, num_words=num_of_words):
    	print "\nTopic", item[0], "==>", item[1]

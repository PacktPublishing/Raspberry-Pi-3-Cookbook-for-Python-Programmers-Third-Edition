
text = "Tokenization is the process of dividing text into a set of meaningful pieces. These pieces are called tokens."

# Sentence tokenization
from nltk.tokenize import sent_tokenize

tokenize_list_sent = sent_tokenize(text) 

print "\nSentence tokenizer:"
print tokenize_list_sent

# Create a new word tokenizer
from nltk.tokenize import word_tokenize
print "\nWord tokenizer:"
print word_tokenize(text)

# Create a new WordPunctokenizer
from nltk.tokenize import WordPunctTokenizer
word_punct_tokenizer = WordPunctTokenizer()
print "\nWord punct tokenizer:"
print word_punct_tokenizer.tokenize(text)

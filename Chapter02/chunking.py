import numpy as np
from nltk.corpus import brown

# Split a text into chunks
def splitter(content, num_of_words):
	words = content.split(' ')
	result = []

	current_count = 0
	current_words = []

	for word in words:
	 current_words.append(word)
	 current_count += 1

         if current_count == num_of_words:
	  result.append(' '.join(current_words))
          current_words = []
	  current_count = 0

        result.append(' '.join(current_words))
        return result


if __name__=='__main__':
  # Read the data from the Brown corpus
  content = ' '.join(brown.words()[:10000])

  # Number of words in each chunk
  num_of_words = 1600

  chunks = []
  counter = 0

  num_text_chunks = splitter(content, num_of_words)
  print "Number of text chunks =", len(num_text_chunks)

import numpy as np
from nltk.corpus import brown
from chunking import splitter

if __name__=='__main__':
    # Read the data from the Brown corpus
    content = ' '.join(brown.words()[:10000])

    # Number of words in each chunk
    num_of_words = 2000
    num_chunks = []
    count = 0
    texts_chunk = splitter(content, num_of_words)

    for text in texts_chunk:
      num_chunk = {'index': count, 'text': text}
      num_chunks.append(num_chunk)
      count += 1

    # Extract document term matrix
    from sklearn.feature_extraction.text import CountVectorizer

    # Extract document term matrix
    from sklearn.feature_extraction.text import CountVectorizer

    vectorizer = CountVectorizer(min_df=5, max_df=.95)
    matrix = vectorizer.fit_transform([num_chunk['text'] for num_chunk in num_chunks])

    vocabulary = np.array(vectorizer.get_feature_names())
    print "\nVocabulary:"
    print vocabulary

    print "\nDocument term matrix:"
    chunks_name = ['Chunk-0', 'Chunk-1', 'Chunk-2', 'Chunk-3', 'Chunk-4']

    formatted_row = '{:>12}' * (len(chunks_name) + 1)
    print '\n', formatted_row.format('Word', *chunks_name), '\n'

    for word, item in zip(vocabulary, matrix.T):
    # 'item' is a 'csr_matrix' data structure
      result = [str(x) for x in item.data]
      print formatted_row.format(word, *result)

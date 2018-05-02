from nltk.stem.porter import PorterStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.snowball import SnowballStemmer

words = ['ability', 'baby', 'college', 'playing', 'is', 'dream', 'election', 'beaches', 'image', 'group', 'happy']

# Compare different stemmers
stemmers = ['PORTER', 'LANCASTER', 'SNOWBALL']

stem_porter = PorterStemmer()
stem_lancaster = LancasterStemmer()
stem_snowball = SnowballStemmer('english')

formatted_row = '{:>16}' * (len(stemmers) + 1)
print '\n', formatted_row.format('WORD', *stemmers), '\n'

for word in words:
	stem_words = [stem_porter.stem(word),
	stem_lancaster.stem(word),
	stem_snowball.stem(word)]
	print formatted_row.format(word, *stem_words)

from collections import Counter
from sklearn.datasets import fetch_20newsgroups
import re
from aion.util.spell_check import SymSpell
corpus = []
for line in fetch_20newsgroups().data:
    line = line.replace('\n', ' ').replace('\t', ' ').lower()
    line = re.sub('[^a-z ]', ' ', line)
    tokens = line.split(' ')
    tokens = [token for token in tokens if len(token) > 0]
    corpus.extend(tokens)
corpus = Counter(corpus)
corpus_dir = '../../data/'
corpus_file_name = 'spell_check_dictionary.txt'
symspell = SymSpell(verbose=10)
symspell.build_vocab(
    dictionary=corpus, 
    file_dir=corpus_dir, file_name=corpus_file_name)
symspell.load_vocab(corpus_file_path=corpus_dir+corpus_file_name)

results = symspell.correction(word='clan')
print(results)

results = symspell.corrections(sentence='8th clan')
print(results)
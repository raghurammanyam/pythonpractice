from collections import Counter
from sklearn.datasets import fetch_20newsgroups
import re

corpus = []
for line in fetch_20newsgroups().data:
    line = line.replace('\n', ' ').replace('\t', ' ').lower()
    line = re.sub('[^a-z ]', ' ', line)
    tokens = line.split(' ')
    tokens = [token for token in tokens if len(token) > 0]
    corpus.extend(tokens)

corpus = Counter(corpus)

import sys, os
def add_aion(curr_path=None):
    if curr_path is None:
        dir_path = os.getcwd()
        target_path = os.path.dirname(os.path.dirname(dir_path))
        if target_path not in sys.path:
#             print('Added %s into sys.path.' % (target_path))
            sys.path.insert(0, target_path)
            
add_aion()

from aion.util.spell_check import SpellCorrector

spell_corrector = SpellCorrector(dictionary=corpus, verbose=1)
abc = spell_corrector.correction(' braveen')
print(abc)

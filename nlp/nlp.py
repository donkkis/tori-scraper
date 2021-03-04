import os
import string
import pandas as pd
import nltk
from nltk import bigrams, trigrams
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from dotenv import load_dotenv
load_dotenv()
from typing import List

STOPWORDS = nltk.corpus.stopwords.words('finnish')

def tokenize(sentence: str) -> List[str]:
    tokens = word_tokenize(sentence.lower())
    tokens = [t for t in tokens if t not in STOPWORDS]
    tokens = [t for t in tokens if t not in string.punctuation]
    return tokens

def get_tags(data: pd.DataFrame = None, col='Title', most_common=200) -> pd.DataFrame:
    """Exctract tags from listing titles, up to frequent 3-grams."""
    if not data:
        data = pd.read_csv(os.getenv('DESCRIPTIONS_PATH'))
    corpus = tokenize(' '.join(data.loc[:, col]))
    tags = pd.DataFrame({'Word': [], 'Count': []})
    fdists = [FreqDist(corpus), FreqDist(list(bigrams(corpus))), FreqDist(list(trigrams(corpus)))]

    for fd in fdists:
        top_n = fd.most_common(most_common)
        common = pd.DataFrame({
            'Word': [' '.join(w[0]) if isinstance(w[0], tuple) else w[0] for w in top_n],
            'Count': [w[1] for w in fd.most_common(most_common)],
        })
        tags = pd.concat([tags, common])

    return tags

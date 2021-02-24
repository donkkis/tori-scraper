import os
import string
import pandas as pd
import nltk
from nltk import bigrams, trigrams
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from dotenv import load_dotenv
load_dotenv()

def get_tags(data: pd.DataFrame = None, col='Title', most_common=200) -> pd.DataFrame:
    """Exctract tags from listing titles, up to frequent 3-grams."""
    if not data:
        data = pd.read_csv(os.getenv('DESCRIPTIONS_PATH'))
    stopwords = nltk.corpus.stopwords.words('finnish')
    corpus = word_tokenize(' '.join(data.loc[:, col]).lower())
    corpus = [t for t in corpus if t not in stopwords]
    corpus = [t for t in corpus if t not in string.punctuation]
    
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
    





import requests
from bs4 import BeautifulSoup
import pandas
import csv

import gensim
from gensim.summarization import summarize
from gensim.summarization import keywords

# # import pandas as pd
import gensim #the library for Topic modelling
from gensim.models.ldamulticore import LdaMulticore
from gensim import corpora, models
import pyLDAvis.gensim_models #LDA visualization library

from nltk.corpus import stopwords

import nltk
import string
from nltk.stem.wordnet import WordNetLemmatizer
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# nltk.download('all')

import warnings
warnings.simplefilter('ignore')
from itertools import chain

def getSummary(vidURL):
    df = webScraped(vidURL)
    pyStr = ""
    for sentence in df['text']:
        pyStr += sentence
    strArr = summarize(pyStr, split=True, ratio=0.8)
    return strArr


def getLDASummary(vidURL):
    df = webScraped(vidURL)

    # # step 2: LDA

    # first: clean our data
    stop = set(stopwords.words('english'))
    exclude = set(string.punctuation)
    lemma = WordNetLemmatizer()

    def clean(text): 
        stop_free = ' '.join([ word for word in text.lower().split() if word not in stop])
        punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
        normalized = ' '.join([lemma.lemmatize(word) for word in punc_free.split()])
        return normalized.split()

        df['text_clean'] = df['text'].apply(clean)

        print(df)

        dictionary = corpora.Dictionary(df['text_clean'])
        print(dictionary.num_nnz)

        doc_term_matrix = [dictionary.doc2bow(doc) for doc in df['text_clean']]
        print(len(doc_term_matrix))

        num_topics = 4

        lda = models.LdaModel(doc_term_matrix, num_topics = num_topics, id2word=dictionary, passes = 50, minimum_probability = 0)

        print(lda.print_topics(num_topics = num_topics))

        # find which articles were marked in which cluster
        lda_corpus = lda[doc_term_matrix]

        print([doc for doc in lda_corpus])

        # threshold
        scores = list(chain(*[[score for topic_id, score in topic] for topic in [doc for doc in lda_corpus]]))

        threshold = sum(scores) / len(scores)

        print(threshold)

        # clusters
        cluster1 = [j for i, j in zip(lda_corpus, df.index) if i[0][1] > threshold]
        cluster2 = [j for i, j in zip(lda_corpus, df.index) if i[1][1] > threshold]
        cluster3 = [j for i, j in zip(lda_corpus, df.index) if i[2][1] > threshold]
        cluster4 = [j for i, j in zip(lda_corpus, df.index) if i[3][1] > threshold]

        print(df.iloc[cluster1])
        print(df.iloc[cluster2])
        print(df.iloc[cluster3])
        print(df.iloc[cluster4])

def webScraped(vidURL):
    URL = vidURL
    r = requests.get(URL)
    print(r.content) # this derives all of the html

    soup = BeautifulSoup(r.content, 'html5lib')

    # encompasses the whole text
    table = soup.find('section', attrs = {'name':'articleBody'})

    pyStr = ""

    with open('test.csv', 'w') as f:
        thewriter = csv.writer(f)

        thewriter.writerow(['text'])

        for row in table.findAll('div', attrs = {'class':'css-1fanzo5'}):
            for eachP in row.findAll('p', attrs = {'class': 'css-axufdj'}):
                    thewriter.writerow([eachP.text])

    dfChart = pandas.read_csv('test.csv')
    return dfChart
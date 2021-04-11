import warnings
warnings.filterwarnings("ignore")

import requests
from bs4 import BeautifulSoup
import pandas
import csv

import gensim
from gensim.summarization import summarize
from gensim.summarization import keywords
from transformers import pipeline

def extractWordsMethod(videoL):
    # webscrape
    URL = videoL
    r = requests.get(URL)
    # ro = requests.post(URL, data=a.encode('utf-8'))
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
                    pyStr += eachP.text

    strWords = keywords(pyStr, words = 5, lemmatize=True)
    return strWords.split('\n')


import re
import sys
import os
import nltk
import string

from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import TweetTokenizer

nltk.download('stopwords')
nltk.download('punkt')

stop_words = set(stopwords.words('english'))

tweetTokenizer = TweetTokenizer()

def tokenize(string_line):
    ''' This function tokenizes the string of text and removes all non alpha-numeric characters
    it takes a string of text as an argument
    it returns a list of all individual words after tokenizing and removing all non alpha-numeric characters'''    
    #return re.findall('[a-zA-Z0-9]+', string_line.lower())
    #return word_tokenize(string_line)
    tokens = tweetTokenizer.tokenize(string_line)
    return list(filter(None, [s.translate(str.maketrans('','',string.punctuation)) for s in tokens]))

def stem(tokens):
    '''This function takes a list of tokens as an argument
    it uses Porter Stemmer to stem the words in the tokens list
    (Here we are using the NLTK library to do this task)
    it retuns a list of all the tokens after stemming'''
    ps = PorterStemmer()
    return [ps.stem(token) for token in tokens]


def preprocess(string, stemming=True, stop=True):
    '''This functioon takes a string of text as an argument, calls the "tokenize" function,
    removes the stop words, then calls the "stem" function to stem the filtered text
    it returns a list of all the preprocessed tokens '''
    tokenized = tokenize(string)
    filtered = [term.lower() for term in tokenized if term not in stop_words or not stop]
    if (stemming):
        filtered = stem(filtered)
    return list(filter(lambda x: x.isalnum(), filtered))
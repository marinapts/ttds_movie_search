#!/usr/bin/env python

import os
import codecs

from nltk import sent_tokenize
import spacy
#spacy_nlp = spacy.load('en_core_web_sm')   # Small model doesn't have any built in vector representations. It generates them by the inputs.
spacy_nlp = spacy.load('en_core_web_md')    # Md model have a medium size of pre defined vectors.
#spacy_nlp = spacy.load('en_core_web_lg')   # Lg model have a large size of pre defined vectors.

class Quotes:
  def __init__(self, quote_path = ''):
    self.quotes = {}
    if os.path.isfile(quote_path):
      self.__read_quotes(quote_path)

  def __read_quotes(self, quote_path):
    """ It reads the quote file in given path. Uptades the quotes dictionary by adding character, sentences tuples. 
    
    Arguments:
        quote_path {string} -- the quote path for a single quote file
    """
    with codecs.open(quote_path, mode="r", encoding="utf-8", errors='ignore') as f:
      lines = f.readlines()
    
    for line in lines:
      splitted = line.replace('\n','').replace('\r', '').split(': ')
      if (len(splitted) > 1):
        if (splitted[0] not in self.quotes.keys()):
          self.quotes[splitted[0]] = ""
        self.quotes[splitted[0]] += ' ' + splitted[1]

    for character, sentences in self.quotes.items():
      self.quotes[character] = sent_tokenize(sentences)


  def find_character_name(self, sentence):
    """ Finds the most similar sentence in the quotes and returns the character name who said the sentence.
        Cosine similarity is used to find most similas sentence.
    
    Arguments:
        sentence {string} -- input sentence found in subtitles.
    
    Returns:
        string -- the character name
    """
    character_similarities = dict()
    for character, docs in self.quotes.items():
      character_similarities[character] = max([spacy_nlp(doc).similarity(spacy_nlp(sentence)) for doc in docs])
    #print(character_similarities)
    return max(character_similarities, key=character_similarities.get)
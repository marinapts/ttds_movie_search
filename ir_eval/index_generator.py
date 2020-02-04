#!/usr/bin/env python

import os
import sys

import preprocessing
import database_functions
import argparse

class IndexGenerator:
    def __init__(self, activate_stemming = True, activate_stop = False):
        """ This class reaeds the documents from db, generates an inverted index and saves it into db.
        
        Keyword Arguments:
            activate_stemming {bool} -- True enables the stemming function over the terms (default: {True})
            activate_stop {bool} -- True enables removing stop words (default: {False})
        """
        self.activate_stemming = activate_stemming
        self.activate_stop = activate_stop
    
    def run_indexing(self):
        """ This function gets the sentences from db and updates the inverted index in db by iterating the sentences.
        """
        cursors = database_functions.get_sentences_cursors()

        for cursor in cursors:
            self.__update_inverted_index(cursor.get('_id'), cursor.get('sentence'))


    def __update_inverted_index(self, document_id, sentence):
        """ This function performs preprocessing on the sentence and updates the inverted index in db. 
        
        Arguments:
            document_id {[type]} -- The document id
            sentence {[type]} -- The sentence.
        """
        preprocessed = preprocessing.preprocess(sentence, stemming=self.activate_stemming, stop=self.activate_stop)
        preprocessed = list(filter(None, preprocessed))

        for pos_in_doc, term in enumerate(preprocessed, start=1):
            if self.activate_stop:
                # Update regular inverted index if removing stop words is enabled.
                database_functions.update_inverted_index(term, document_id, pos_in_doc)
            else:
                # Update inverted index with stop words if removing stop words is disabled.
                database_functions.update_inverted_index_stop(term, document_id, pos_in_doc)


def run_with_arguments(stem, stop):
    indexGen = IndexGenerator(activate_stop=stop, activate_stemming=stem)
    indexGen.run_indexing()

parser = argparse.ArgumentParser(description='Inverted Index Generator')
parser.add_argument('--stemming', nargs="?", type=bool, default=True, help='Activate stemming')
parser.add_argument('--remove_stopwords', nargs="?", type=bool, default=False, help='Remove stopwords')
args = parser.parse_args()

run_with_arguments(args.stemming, args.remove_stopwords)

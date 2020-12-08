#!/usr/bin/env python

import os
import sys
import json
import pickle

#import pandas as pd

from ir_eval import preprocessing, database_functions
import argparse
import logging

logging.basicConfig(filename='result.log', level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class IndexGenerator:
    def __init__(self, activate_stemming = True, activate_stop = False, start_index=0):
        """ This class reaeds the documents from db, generates an inverted index and saves it into db.
        
        Keyword Arguments:
            activate_stemming {bool} -- True enables the stemming function over the terms (default: {True})
            activate_stop {bool} -- True enables removing stop words (default: {False})
        """
        self.activate_stemming = activate_stemming
        self.activate_stop = activate_stop
        self.start = start_index

        self.temp = dict()
    
    def run_indexing(self):
        """ This function gets the sentences from db and updates the inverted index in db by iterating the sentences.
        """

        batch = 100000
        for i in range(self.start, 776):
            logging.info("loading: " + str(i+1) + "/" + str(776))

            cursors = database_functions.get_sentences_cursors(i * batch, batch)
            for cursor in cursors:
                self.__load_tempfile(cursor.get('_id'), cursor.get('sentence'), cursor.get('movie_id'))

            if (i+1)%15 == 0:
                self.__regularize_dict()
                self.__save_pickle(str(i-14) + "-" + str(i+1) + "-insert")

        self.__regularize_dict()
        self.__save_pickle("last")

    def __load_tempfile(self, doc_id, sentence, movie_id):
        preprocessed = preprocessing.preprocess(sentence, stemming=self.activate_stemming, stop=self.activate_stop)
        preprocessed = list(filter(None, preprocessed))

        word_count = len(preprocessing.preprocess(sentence, stemming=False, stop=False))
        
        for term in set(preprocessed):
            positions = [n for n,item in enumerate(preprocessed) if item==term]
            self.temp[term] = self.temp.get(term, {
                'term': term,
                'doc_count': 0,
                'movies': dict()
            })
            self.temp[term]['doc_count'] += 1
            self.temp[term]['movies'][movie_id] = self.temp[term]['movies'].get(movie_id, {'_id': movie_id, 'doc_count': 0, 'sentences': list()})
            self.temp[term]['movies'][movie_id]['doc_count'] += 1
            self.temp[term]['movies'][movie_id]['sentences'].append({
                        '_id': doc_id,
                        'len': word_count,
                        'pos': positions
                    })
                    
    def __regularize_dict(self):
        for value in self.temp.values():
            value['movies'] = list(value['movies'].values())

    def __save_pickle(self, name):
        with open(name + '.pickle', 'wb') as handle:
            pickle.dump(list(self.temp.values()), handle, protocol=pickle.HIGHEST_PROTOCOL)
        self.temp.clear()

def run_with_arguments(stem, stop, start):
    indexGen = IndexGenerator(activate_stop=stop, activate_stemming=stem, start_index=start)
    indexGen.run_indexing()

parser = argparse.ArgumentParser(description='Inverted Index Generator')
parser.add_argument('--stemming', nargs="?", type=str, default='True', help='Activate stemming')
parser.add_argument('--remove_stopwords', nargs="?", type=str, default='False', help='Remove stopwords')
parser.add_argument('--start', nargs="?", type=int, default=0, help='Start batch index')
args = parser.parse_args()

run_with_arguments(eval(args.stemming), eval(args.remove_stopwords), args.start)

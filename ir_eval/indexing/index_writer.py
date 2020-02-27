#!/usr/bin/env python

import os
import sys
import logging
import preprocessing
import database_functions
import argparse
import pickle
from pymongo import MongoClient

logging.basicConfig(filename='result.log', level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

client = MongoClient('mongodb://admin:iamyourfather@167.71.139.222:27017/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false')
inverted_index = client.ttds.inverted_index

class IndexWriter:
    def __init__(self, path):
        self.dir = path
        self.temp = dict()

    def __iterate_dir(self):
        """ It itertes all of the leaf files under the root path directory.
        
        Yields:
            string -- leaf path
        """
        for file in os.listdir(self.dir):
            filename = os.fsdecode(file)
            if filename.endswith(".pickle"): 
                yield os.path.join(self.dir, filename), filename

    def __read_pickle(self, path):
        logging.info(path + ' is processing...')
        with open(path, 'rb') as handle:
            file = pickle.load(handle)
        return file

    def __flush_db(self):
        global inverted_index
        logging.info('DB flushing...')
        inverted_index.insert_many(self.temp)
        self.temp.clear()
        logging.info("DB flushed!")

    def write_index(self):
        for path, filename in self.__iterate_dir():
            self.temp = self.__read_pickle(path)
            self.__flush_db()

asd = IndexWriter("/Users/oguz/Documents/ttds_movie_search/ir_eval")
asd.write_index()
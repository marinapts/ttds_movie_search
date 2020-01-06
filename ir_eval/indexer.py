#!/usr/bin/env python

import os
import sys
sys.path.insert(1, './')

import preprocessing

import re
import codecs
import pprint
import json
import datetime
import pickle

class SrtIndexer:
  def __init__(self, path = os.path.dirname(os.path.abspath(__file__))):
    """ The constructor function of the class.
    
    Arguments:
        path {string} -- Optional path argument to be indexed. It is set current working directory bu default.
    """
    self.set_path(path)
    self.inverted_index = {}
    self.word2id = {}
    self.json_name = "inverted_index.pickle"
    self.activate_stem = True
    self.activate_stop = True
    self.reindex = False

  def enableStemming(self, boolean):
    """ Enable/disable stemming. By default stemming is enabled.
    
    Arguments:
        boolean {boolean} -- True to enable stemming
    """
    self.activate_stem = boolean

  def enableStopping(self, boolean):
    """ Enable/disable stopping. By default stopping is enabled.
    
    Arguments:
        boolean {boolean} -- True to enable stopping
    """
    self.activate_stop = boolean

  def set_path(self, path):
    """ Set the root path to be crawled and indexed.
    
    Arguments:
        path {string} -- the root path for srt files.
    """
    self.path = path

  def enforce_reindex(self, boolean):
    """ This sets the boolean flag to reindex data even if already indexed.
    
    Arguments:
        boolean {boolean} -- True to enable enforcing
    """
    self.reindex = boolean

  def get_inverted_index(self):
    """ Returns the inverted index.
    
    Returns:
        dictionary -- the inverted index.
    """
    return self.inverted_index

  def __iterate_files(self):
    """ It itertes all of the leaf files under the root path directory.
    
    Yields:
        string -- leaf path
    """
    root = os.walk(self.path)
    for dir_entry in root:
      for fname in dir_entry[2]:
        yield os.path.join(dir_entry[0], fname)

  def build_index(self):
    """ Sets the inverted index. If an inverted index file saved before and reindexing is not enforced, 
        it loads the old index file. Otherwise, It iterates all srt files, creates a new inverted index 
        and saves it.
    """
    old_path = os.path.join(self.path, self.json_name)
    if os.path.isfile(old_path) and not self.reindex:
      self.inverted_index = self.__json_load(old_path)
      print(sys.getsizeof(self.inverted_index))
    else:
      for element in self.__iterate_files():
          if (element.endswith('.srt')):
            self.__index_single_file(element)
      self.__pickle_write(self.inverted_index, old_path)

  def __index_single_file(self, file_path):
    """ It indexes only one file. It is called for each file in build_index function.
    
    Arguments:
        file_path {string} -- the srt file path.
    """
    file_name = os.path.splitext(os.path.basename(file_path))[0]; 

    with codecs.open(file_path, mode="r", encoding="utf-8", errors='ignore') as f:
      lines = f.readlines()

    data = self.__reformat_srt_file(lines)
    self.__save_to_db(data, file_name)
    data = [preprocessing.preprocess(x[1], stemming=True, stop=False) for x in data]
    data = list(filter(None, data))
    self.__update_word_list(data)
    self.__update_inverted_index(data, file_name)
    #String[] words = str.split("\s\n+");

  def __reformat_srt_file(self, raw_lines):
    lines = []
    regex_string = '\d\d:\d\d:\d\d,\d\d\d\s*-->\s*\d\d:\d\d:\d\d,\d\d\d\r*\n*'
    regex_end_sentence = '.*(?<!\.{2})[.?!"]\n*\r*$'
    regex_numeric = '\d+\r*\n*'
    regex_empty = '^\s*\r*\n*$'
    pattern_time = re.compile(regex_string)
    pattern_end_sentence = re.compile(regex_end_sentence)
    pattern_numeric = re.compile(regex_numeric)
    pattern_empty = re.compile(regex_empty)

    temp = ""
    temp_time = None
    for line in raw_lines:
      if pattern_time.match(line):
        time = line.split(' --> ')[0]
        start_time = datetime.datetime.strptime(time, '%H:%M:%S,%f')
        if temp_time == None:
          temp_time = start_time.timestamp()
      elif not pattern_numeric.match(line) and not pattern_empty.match(line):
        temp += line.replace('\n', ' ').replace('\r', '').replace('...', '')
        if pattern_end_sentence.match(line):
          temp = temp.strip()
          if temp.startswith('-'):
            temp = temp[1:]
          lines.append([temp_time, temp])
          temp = ""
          temp_time = None
    return lines

  def __save_to_db(self, data, title):
    a = 0
    #for line_number, sentence in enumerate(data, start=1):
      #print(str(line_number) + ' ' + sentence[1])

  def __update_word_list(self, word_lists):
    """ It updates the word2id dictionary by adding new words in word_lists.
    
    Arguments:
        word_lists {list} -- list of lists, containing the words for each subtitle section.
    """
    unique = set([y for x in word_lists for y in x])
    for word in unique:
      if word not in self.word2id.keys():
          self.word2id[word] = len(self.word2id)
      ## Save as binary file, update id2word

  def __update_inverted_index(self, word_lists, file_name):
    """ It updates the inverted index by adding new terms and new positional document indices.
    
    Arguments:
        word_lists {list} -- list of lists, containing the words for each subtitle section.
        file_name {string} -- the name of the indexed srt file, it is used to create document id. 
    """
    for word, id in self.word2id.items():
      if word not in self.inverted_index.keys():
        #self.inverted_index[id] = dict()
        self.inverted_index[word] = dict()

    for line_number, sent in enumerate(word_lists, start=1):
        docid = file_name + '_' + str(line_number)
        for pos_in_doc, term in enumerate(sent, start=1):
          #index_term = self.word2id[term]
          index_term = term
          if docid not in self.inverted_index[index_term].keys():
              self.inverted_index[index_term][docid] = []

          self.inverted_index[index_term][docid].append(pos_in_doc)

  def __json_write(self, data, path):
    """ write data to path in json format.
    
    Arguments:
        data {dictionary} -- the dictionary
        path {string} -- path
    """
    json.dump(data, open(path, 'w'))

  def __json_load(self, path):
    """ It loads and returns a json data in dictionary structure.
    
    Arguments:
        path {string} -- the path of the json data
    
    Returns:
        dictionary -- the dictionary created from the json data.
    """
    return json.load(open(path))

  def __pickle_write(self, data, path):
    """ write data to path in pickle format.
    
    Arguments:
        data {dictionary} -- the dictionary
        path {string} -- path
    """
    with open(path, 'wb') as handle:
      pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

  def __pickle_load(self, path):
    """ It loads and returns a pickle data in dictionary structure.
    
    Arguments:
        path {string} -- the path of the pickle data
    
    Returns:
        dictionary -- the dictionary created from the pickle data.
    """
    with open(path, 'rb') as handle:
      b = pickle.load(handle)
    return b

ab = SrtIndexer("/Users/oguz/Documents/ttds_movie_search/ir_eval/data/subtitles/")
#ab.enforce_reindex(True)
ab.build_index()
#pprint.pprint(ab.get_inverted_index())
#!/usr/bin/env python

import os
import sys

import preprocessing
import database_functions

import re
import codecs
import pprint
import json
import datetime
import pickle
import logging

logging.basicConfig(filename="result.log", level=logging.NOTSET)

class SubtitleParser:
  def __init__(self, root_subtitle_path = os.path.dirname(os.path.abspath(__file__))):
    """ This class parses the subtitles files and writes them into db.
    
    Arguments:
        path {string} -- Optional path argument to be indexed. It is set current working directory bu default.
    """
    self.set_path(root_subtitle_path)

  def set_path(self, path):
    """ Set the root path to be crawled and indexed.
    
    Arguments:
        path {string} -- the root path for srt files.
    """
    self.path = path

  def __iterate_files(self):
    """ It itertes all of the leaf files under the root path directory.
    
    Yields:
        string -- leaf path
    """
    root = os.walk(self.path)
    for dir_entry in root:
      for fname in dir_entry[2]:
        yield os.path.join(dir_entry[0], fname), os.path.join(dir_entry[0].replace('subtitles', 'quotes'), fname.replace('srt','txt'))

  def run_parser(self):
    """ Sets the inverted index. If an inverted index file saved before and reindexing is not enforced, 
        it loads the old index file. Otherwise, It iterates all srt files, parses and saves them into db.
    """
    for element, quote_path in self.__iterate_files():
      if (element.endswith('.srt')):
        self.__index_single_file(element, quote_path)

  def __index_single_file(self, file_path, quote_path):
    """ It indexes only one file. It is called for each file in build_index function.
    
    Arguments:
        file_path {string} -- the srt file path.
    """
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    with codecs.open(file_path, mode="r", encoding="utf-8-sig", errors='ignore') as f:
      lines = f.readlines()

    regex_empty = '^\s*\r*\n*$'
    regex_numeric = '\d+\r*\n*'
    pattern_numeric = re.compile(regex_numeric)
    pattern_empty = re.compile(regex_empty)

    data = []

    first = None
    i = 0
    while first is None:
      if not pattern_empty.match(lines[i]):
        first = lines[i]
      i += 1

    logging.info(file_path + ' being written to db...')

    if not pattern_numeric.match(first):
      data = self.__reformat_sub_file(lines)
    else:
      data = self.__reformat_srt_file(lines)

    if len(data) > 0:
      database_functions.update_sentences(data, file_name)
      logging.info("done!")
    else:
      logging.info("Not completed!")

  def __reformat_srt_file(self, raw_lines):
    lines = []
    regex_string = '\d\d:\d\d:\d\d,\d\d\d\s*-->\s*\d\d:\d\d:\d\d,\d\d\d\r*\n*'
    regex_end_sentence = '.*(?<!\.{2})[.?!"]\n*\r*$'
    regex_numeric = '\d+\r*\n*'
    regex_empty = '^\s*\r*\n*$'
    pattern_html = re.compile(r'<[^>]+>')
    pattern_square = re.compile(r'\[[^\]]+]')
    pattern_time = re.compile(regex_string)
    pattern_end_sentence = re.compile(regex_end_sentence)
    pattern_numeric = re.compile(regex_numeric)
    pattern_empty = re.compile(regex_empty)

    temp = ""
    temp_time = None
    dquote = False
    appended = False
    for line in raw_lines:
      if pattern_time.match(line):

        time = line.split('-->')[0].strip()
        try:
          time_obj = datetime.datetime.strptime(time, '%H:%M:%S,%f')
          if temp_time == None:
            temp_time = int(time_obj.hour * 3600000 + time_obj.minute * 60000 + time_obj.second * 1000 + time_obj.microsecond/1000)
        except:
          logging.error('incorrect time format: ' + time)
      elif not pattern_numeric.match(line) and not pattern_empty.match(line):
        sentence = pattern_square.sub('', pattern_html.sub('', line))
        temp += sentence.replace('\n', ' ').replace('\r', '').replace('...', '')

        if pattern_end_sentence.match(sentence):
          temp = temp.strip()
          if temp.startswith('-'):
            temp = temp[1:]

          lines.append([temp_time, temp])
          appended = True
          temp = ""
          temp_time = None

    return lines

  def __reformat_sub_file(self, raw_lines, fps=24.0):
    lines = []
    regex_frame_sentence = "{(.*?)}.*}(.*)"
    regex_empty = '^\s*\r*\n*$'
    regex_end_sentence = '.*(?<!\.{2})[.?!"]\n*\r*$'

    pattern_frame_sentence = re.compile(regex_frame_sentence)
    pattern_empty = re.compile(regex_empty)
    pattern_end_sentence = re.compile(regex_end_sentence)

    temp = ""
    temp_time = None
    dquote = False
    for line in raw_lines:
      if not pattern_empty.match(line):
        match = pattern_frame_sentence.match(line)
        if match is not None:
          frame, sentence = match.groups()
          temp += sentence.replace('\n', '').replace('\r', '').replace('|', ' ')
          if temp_time == None:
            temp_time = int(frame) * 1000 / fps

          if line.count("\"") & 1: # if odd number of double quote used, dquote is inversed.
            dquote = not dquote
          if pattern_end_sentence.match(sentence) and not dquote:
            temp = temp.strip()
            if temp.startswith('-'):
              temp = temp[1:]
            lines.append([int(temp_time), temp])
            temp = ""
            temp_time = None
            dquote = False
    return lines

sp = SubtitleParser("/home/new_sub/subtitles")
sp.run_parser()

#pprint.pprint(ab.get_inverted_index())

#cd = Quotes('/Users/oguz/Documents/ttds_movie_search/ir_eval/data/quotes/0/0/7/tt0073582.txt')
#cd.find_character_name("a woman is going to be free so she can")
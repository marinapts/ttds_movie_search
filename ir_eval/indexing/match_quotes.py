import os
import pandas 
import sys
from ir_eval import preprocessing 
from csv import writer
from joblib import Parallel, delayed, parallel_backend
from tqdm import tqdm

sentences = pandas.read_csv("/home/oguz/ttds_movie_search/ir_eval/data/sentences.csv")

def get_sentences_by_movie(movie_id):
    return sentences[sentences['movie_id'] == movie_id]

def iterate_files(path):
    root = os.walk(path)
    for dir_entry in root:
      for fname in dir_entry[2]:
        yield os.path.join(dir_entry[0], fname), fname.replace('.txt','')

def get_similarity(str1, str2):
    str1 = preprocessing.preprocess(str1, stemming=False, stop=False) 
    str2 = preprocessing.preprocess(str2, stemming=False, stop=False)

    x1 = set(str1)
    x2 = set(str2)
    rvector = x1.union(x2)
    l1 =[]
    l2 =[]

    for w in rvector: 
        if w in x1: 
            l1.append(1) # create a vector 
        else: 
            l1.append(0) 
        if w in x2: 
            l2.append(1) 
        else: 
            l2.append(0) 
    

    # cosine formula  
    c = 0
    for i in range(len(rvector)): 
        c+= l1[i]*l2[i] 
    divider = float((sum(l1)*sum(l2))**0.5) 
    if divider == 0:
        return 0

    return c / divider

def find_most_similar(quote, movie_id):
    movie_sentences = get_sentences_by_movie(movie_id)
    similar_id = -1
    max_similarity = 0.80
    for row_index, row in movie_sentences.iterrows():
        _id = row['_id']
        sentence = row['sentence']
        similarity = get_similarity(quote, sentence)
        if similarity > max_similarity:
            similar_id = _id
            max_similarity = similarity
        
    return similar_id

def append_to_csv(sentence_id, character):
    with open("quote_match.csv", 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow([sentence_id, character])

def match_quote(quote_line, movie_id):
    if ':' in quote_line:
        split = quote_line.replace("\n","").replace("\r", "").strip().split(':')
        character = split[0]
        quote = split[1]
        sentence_id = find_most_similar(quote, movie_id)
        if sentence_id > -1:
            append_to_csv(sentence_id, character)

def paralel_function(quote_path, movie_id):
    with open(quote_path) as quote_file:
        for line in quote_file:
            match_quote(line, movie_id)


with parallel_backend('multiprocessing', n_jobs=-1):
    Parallel()(delayed(paralel_function)(quote_path, movie_id) for quote_path, movie_id in tqdm(iterate_files("/home/oguz/ttds_movie_search/ir_eval/data/quotes"), total=218645))
 
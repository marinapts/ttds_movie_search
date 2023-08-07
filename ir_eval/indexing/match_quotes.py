import os
import pandas 
import sys
from ir_eval import preprocessing 
from csv import writer, reader, DictReader
from joblib import Parallel, delayed, parallel_backend
from tqdm import tqdm
import codecs

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

def append_to_csv(sentence_id, character):
    with open("quote_match.csv", 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow([sentence_id, character])

def similarity(quote_line, sentence):
    if ':' in quote_line:
        split = quote_line.replace("\n","").replace("\r", "").strip().split(':')
        character = split[0]
        quote = split[1]
        return get_similarity(quote, sentence), character
    else:
        return 0, ''

def paralel_function(line, index):
    sentence_id =  line[0]
    movie_id = line[1]
    sentence = line[2]
    try:
        if index > 0:
            first3 = movie_id[2:5]
            quote_path = "/home/oguz/ttds_movie_search/ir_eval/data/quotes/" + first3[0] + "/" + first3[1] + "/" + first3[2] + "/" + movie_id + ".txt"
            with open(quote_path) as quote_file:
                max_similarity = 0.80
                character = ""
                for line in quote_file:
                    if line != "":
                        sim, name = similarity(line, sentence)

                        if sim > max_similarity:
                            max_similarity = sim
                            character = name
                
                if character != "":
                    append_to_csv(sentence_id, character)
    except:
        print('Error occured')



start = 0

sentences = pandas.read_csv("/home/oguz/ttds_movie_search/ir_eval/data/sentences.csv", skiprows=start)


with parallel_backend('multiprocessing', n_jobs=-1):
    Parallel()(delayed(paralel_function)(row, i) for i, row in tqdm(sentences.iterrows(), total=77584425 - start))
 
from keras.preprocessing.text import Tokenizer
from pickle import dump, load
import os
import io
import string
from nltk.tokenize import TweetTokenizer

text_file = io.open('test.txt', 'r', encoding='utf-8')
tweetTokenizer = TweetTokenizer()

# hyperparameters
seq_len = 1  # 1 for bigrams, 2 for trigrams, and so on
batch_size = 5
# Number of generated sentences at a time
num_sentences = 100


def get_sentence():
    # read the next sentence from file. If file is finished, load the file again and start reading from beginning.
    global text_file
    line = text_file.readline()
    #    print(line)
    done = False
    if line == '':  # end of file reached. Start reading from the beginning again.
        done = True
        text_file = io.open('test.txt', 'r',
                            encoding='utf-8')  # perhaps run a command to shuffle the sentences file before opening it.
        line = text_file.readline()
    return line, done


def get_sentences(n):
    # get n sentences in a string format joined with spaces
    sentences = ''
    for i in range(n):
        s, done = get_sentence()
        sentences += s + ' '
        if done:
            return sentences, True
    return sentences, False
    # return ' '.join([get_sentence() for i in range(n)])  # <- this should be slower, I think


def tokenize(string_line):
    ''' This function tokenizes the string of text and removes all non alpha-numeric characters
    it takes a string of text as an argument
    it returns a list of all individual words after tokenizing and removing all non alpha-numeric characters'''
    tokens = tweetTokenizer.tokenize(string_line)
    return list(filter(None, [s.translate(str.maketrans('', '', string.punctuation)) for s in tokens]))


# text, _ = get_sentences(num_sentences)
# tokens = tokenize(text)
# tokens.pop(0)

# Building the generator
train_len = seq_len + 1
def text_generator():
    done = False
    while not done:
        text, done = get_sentence()
        tokens = tokenize(text)
        for i in range(train_len, len(tokens)+1):
            seq = tokens[i - train_len:i]
            yield seq


# Keras Tokenizer, which encodes words into numbers
tokenizer = Tokenizer()
tokenizer.fit_on_texts(text_generator())

print(tokenizer.word_counts)

# Saving the tokenizer model
dump(tokenizer, open('tokenizer_Model', 'wb'))
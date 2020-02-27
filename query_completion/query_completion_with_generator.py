from keras.preprocessing.text import Tokenizer
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import LSTM, Dense, Activation, Embedding
from keras import optimizers
from keras.callbacks import ModelCheckpoint
from keras import backend
from sklearn.preprocessing import LabelBinarizer
from sklearn.metrics import classification_report
from pickle import dump, load
from nltk.tokenize import word_tokenize
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import numpy as np
import os
import io
import nltk
import string

text_file = io.open('test.txt', 'r', encoding='utf-8')
tokenizer = load(open('tokenizer_Model','rb'))
stop_words = set(stopwords.words('english'))
tweetTokenizer = TweetTokenizer()

# hyperparameters
seq_len = 1  # 1 for bigrams, 2 for trigrams, and so on
train_len = seq_len + 1
batch_size = 5
num_epochs = 50
# Number of generated sentences at a time
num_sentences = 100

#tokenizer = Tokenizer()  # load tokenizer from file instead
# Collecting some information
vocabulary_size = len(tokenizer.word_counts)

######################### Pre-Processing #########################

def get_sentence():
    # read the next sentence from file. If file is finished, load the file again and start reading from beginning.
    global text_file
    line = text_file.readline().lower()
    #    print(line)
    if line == '':  # end of file reached. Start reading from the beginning again.
        text_file = io.open('test.txt', 'r',
                            encoding='utf-8')  # perhaps run a command to shuffle the sentences file before opening it.
        line = text_file.readline()
    return line


def get_sentences(n):
    # get n sentences in a string format joined with spaces
    sentences = ''
    for i in range(n):
        sentences += get_sentence() + ' '
    return sentences


# return ' '.join([get_sentence() for i in range(n)])  # <- this should be slower, I think

def tokenize(string_line):
    ''' This function tokenizes the string of text and removes all non alpha-numeric characters
	it takes a string of text as an argument
	it returns a list of all individual words after tokenizing and removing all non alpha-numeric characters'''
    tokens = tweetTokenizer.tokenize(string_line)
    return list(filter(None, [s.translate(str.maketrans('', '', string.punctuation)) for s in tokens]))


def preprocess(string: str, stop=True):
    '''This functioon takes a string of text as an argument, calls the "tokenize" function,
	removes the stop words, then calls the "stem" function to stem the filtered text
	it returns a list of all the preprocessed tokens '''
    tokenized = tokenize(string)
    filtered = [term for term in tokenized if term not in stop_words or not stop]
    return list(filter(lambda x: x.isalnum(), filtered))


######################### Data Generator #########################

def data_generator():
#    global tokenizer  # you have to load tokenizer from file at the top of this script
    total_times = 0
    bigrams = []  # or tri-grams or whatever, but in this case it will be a list of lists of 2 strings
    while True:  # while total_times < 100000: I don't know how many times this loop should happen. Try and see. Hopefully it can be run forever
        total_times += 1
        # keep looping until we reach our batch size
        text = get_sentence()
        tokens = tokenize(text)

        for i in range(train_len, len(tokens)+1):
            seq = tokens[i - train_len:i]
            if len(seq) == train_len:  # safety check: only add bigrams
                bigrams.append(seq)
            if len(bigrams) >= batch_size:  # batch size reached. Yield!
                train_inputs = []
                train_targets = []
                for seq in tokenizer.texts_to_sequences_generator(bigrams):
                    # Splitting the sequences into inputs and target
                    train_input = seq[:-1]
                    train_target = seq[-1]
                    train_target = to_categorical(train_target, num_classes=vocabulary_size + 1)
                    train_inputs.append(train_input)
                    train_targets.append(train_target)
                bigrams.clear()
                yield train_inputs, train_targets





#for x, y in data_generator():
#    print (x,y)
# train_inputs, train_targets, vocabulary_size, tokenizer = data_generator(text_file, batch_size)
# print(train_targets)


# text = get_sentences(num_sentences)  # Comment: try getting the sentences in chunks like this and repeating the fitting process.
# #print(text)
# tokens = tokenize(text)
# tokens.pop(0)

######################### Building the Sequence #########################
#
# #Converting the tokens to sequences
# train_len = seq_len+1
# text_sequences = []
# for i in range(train_len,len(tokens)):
#     seq = tokens[i-train_len:i]
#     text_sequences.append(seq)
#
# sequences = {}
# count = 1
# for i in range(len(tokens)):
#     if tokens[i] not in sequences:
#         sequences[tokens[i]] = count
#         count += 1
#
# #Keras Tokenizer, which encodes words into numbers
# tokenizer = Tokenizer()
# tokenizer.fit_on_texts(text_sequences)
# sequences = tokenizer.texts_to_sequences(text_sequences)
#
# #Collecting some information
# vocabulary_size = len(tokenizer.word_counts)
#
# n_sequences = np.empty([len(sequences),train_len], dtype='int32')
# for i in range(len(sequences)):
#     n_sequences[i] = sequences[i]
#
# #Splitting the sequences into inputs and target
# train_inputs = n_sequences[:,:-1]
# train_targets = n_sequences[:,-1]
# train_targets = to_categorical(train_targets, num_classes=vocabulary_size+1)
#
# seq_len = train_inputs.shape[1]

######################### The Model #########################

def create_model(vocabulary_size, seq_len):
    model = Sequential()
    model.add(Embedding(vocabulary_size, seq_len, input_length=seq_len))
    #    model.add(Embedding(batch_size, seq_len,input_length=seq_len))
    model.add(LSTM(50, return_sequences=True))
    model.add(LSTM(50))
    model.add(Dense(50, activation='relu'))
    model.add(Dense(vocabulary_size, activation='softmax'))
    opt_adam = optimizers.adam(lr=0.001)
    model.compile(loss='categorical_crossentropy', optimizer=opt_adam, metrics=['accuracy'])
    model.summary()
    return model


######################### The Main Code #########################

# Creating the model
model = create_model(vocabulary_size + 1, seq_len)

# Saving the model
path = os.path.join('checkpoints', 'word_pred_Model1.h5')

# Saving the checkpoints
checkpoint = ModelCheckpoint(path, monitor='loss', verbose=1, save_best_only=True, mode='min')

# Fitting the model
model.fit_generator(data_generator(), steps_per_epoch = vocabulary_size // batch_size, epochs=num_epochs,
                    shuffle=True, verbose=1, callbacks=[checkpoint])

## Saving the tokenizer model
#dump(tokenizer, open('tokenizer_Model0', 'wb'))

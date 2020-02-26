from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import LSTM, Dense, Activation, Embedding
from keras import optimizers
from keras.callbacks import ModelCheckpoint
from keras import backend
from pickle import dump,load
import os
import io
import nltk
import string
from nltk.tokenize import word_tokenize
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import numpy as np

text_file = io.open('sentences.txt', 'r', encoding='utf-8')
stop_words = set(stopwords.words('english'))
tweetTokenizer = TweetTokenizer()

#hyperparameters
seq_len = 2 # 2 for bigrams, 3 for trigrams, and so on
batch_size = 5
#Number of generated sentences at a time
num_sentences = 5



######################### Pre-Processing #########################

def get_sentence():
    # read the next sentence from file. If file is finished, load the file again and start reading from beginning.
    global text_file
    line = text_file.readline()
#    print(line)
    if line == '':  # end of file reached. Start reading from the beginning again.
        text_file = io.open('sentences.txt', 'r', encoding='utf-8')  # perhaps run a command to shuffle the sentences file before opening it.
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
    return list(filter(None, [s.translate(str.maketrans('','',string.punctuation)) for s in tokens]))

def preprocess(string: str, stop=True):
    '''This functioon takes a string of text as an argument, calls the "tokenize" function,
    removes the stop words, then calls the "stem" function to stem the filtered text
    it returns a list of all the preprocessed tokens '''
    tokenized = tokenize(string)
    filtered = [term for term in tokenized if term not in stop_words or not stop]
    return list(filter(lambda x: x.isalnum(), filtered))

text = get_sentences(num_sentences)  # Comment: try getting the sentences in chunks like this and repeating the fitting process.
#print(text)
tokens = preprocess(text)
tokens.pop(0)

######################### Building the Sequence #########################

#Converting the tokens to sequences
train_len = seq_len+1
text_sequences = []
for i in range(train_len,len(tokens)):
    seq = tokens[i-train_len:i]
    text_sequences.append(seq)

sequences = {}
count = 1
for i in range(len(tokens)):
    if tokens[i] not in sequences:
        sequences[tokens[i]] = count
        count += 1  

#Keras Tokenizer, which encodes words into numbers     
tokenizer = Tokenizer()
tokenizer.fit_on_texts(text_sequences)
sequences = tokenizer.texts_to_sequences(text_sequences) 

#Collecting some information   
vocabulary_size = len(tokenizer.word_counts)

n_sequences = np.empty([len(sequences),train_len], dtype='int32')
for i in range(len(sequences)):
    n_sequences[i] = sequences[i]
    
#Splitting the sequences into inputs and target
train_inputs = n_sequences[:,:-1]
train_targets = n_sequences[:,-1]
train_targets = to_categorical(train_targets, num_classes=vocabulary_size+1)

seq_len = train_inputs.shape[1]

######################### The Model #########################

def create_model(vocabulary_size, seq_len):
    model = Sequential()
    model.add(Embedding(vocabulary_size, seq_len,input_length=seq_len))
#    model.add(Embedding(batch_size, seq_len,input_length=seq_len))

    model.add(LSTM(50,return_sequences=True))
    model.add(LSTM(50))
    model.add(Dense(50,activation='relu'))
    model.add(Dense(vocabulary_size,activation='softmax'))
    opt_adam = optimizers.adam(lr=0.001)
    #You can simply pass 'adam' to optimizer in compile method. Default learning rate 0.001
    #But here we are using adam optimzer from optimizer class to change the LR.
    model.compile(loss='categorical_crossentropy',optimizer=opt_adam,metrics=['accuracy'])
    model.summary()
    return model

######################### The Main Code #########################

#Creating the model
model = create_model(vocabulary_size+1,seq_len)

#Saving the model
path = os.path.join('checkpoints', 'word_pred_Model3.h5')

#Saving the checkpoints
checkpoint = ModelCheckpoint(path, monitor='loss', verbose=1, save_best_only=True, mode='min')

#Fitting the model
model.fit(train_inputs,train_targets,batch_size=128,epochs=500,verbose=1,callbacks=[checkpoint])

#Saving the tokenizer model
dump(tokenizer,open('tokenizer_Model3','wb')) 
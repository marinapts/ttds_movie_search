from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
from pickle import load
import os

model_path = os.path.join('checkpoints', 'word_pred_Model1.h5')
model = load_model(model_path)
tokenizer = load(open('tokenizer_Model','rb'))

seq_len = 1
num_gen_words = 1

def predict_next_word(seed_text):
    output_text = []
    input_text = seed_text
    for i in range(num_gen_words):
        encoded_text = tokenizer.texts_to_sequences([input_text])[0]
        pad_encoded = pad_sequences([encoded_text], maxlen=seq_len,truncating='pre')
        pred_word_ind = model.predict_classes(pad_encoded,verbose=0)[0]
        pred_word = tokenizer.index_word[pred_word_ind]
        input_text += ' '+pred_word
        output_text.append(pred_word) #keeping this in case we decided to change the number of predicted words
    return ' '.join(output_text) #keeping this in case we decided to change the number of predicted words

if __name__ == '__main__':
    # You can add some print tests here to see that predict_next_word(word) is working as expected
    print(predict_next_word("poor"))
    print(predict_next_word("cat"))
    print(predict_next_word("shall"))
    print(predict_next_word("mother"))

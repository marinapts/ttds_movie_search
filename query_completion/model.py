
# TODO: load your model here
model = None


def predict_next_word(word):
    # TODO: use the model here to predict the next word.
    # Return: the next word or None if model can't predict it for any reason.
    return 'father'

if __name__ == '__main__':
    # You can add some print tests here to see that predict_next_word(word) is working as expected
    print(predict_next_word("I"))
    print(predict_next_word("am"))
    print(predict_next_word("your"))
    print(predict_next_word("father"))

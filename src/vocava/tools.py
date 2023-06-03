import nltk
from nltk.tokenize import sent_tokenize, TreebankWordTokenizer

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


def tag_parts_of_speech(story):
    tokenizer = TreebankWordTokenizer()
    pos_tagged = []
    for sentence in sent_tokenize(story):
        words = tokenizer.tokenize(sentence)
        pos_tagged.append(nltk.pos_tag(words))
    return pos_tagged

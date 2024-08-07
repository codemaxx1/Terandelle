

# imports
print("before importing spacy")
import spacy
print("after importing psacy")
import nltk
nltk.download('popular')  # This command downloads the most popular datasets and models

from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag



class TextProsessing:

    def preprocess(input_sentence):
        words = word_tokenize(input_sentence)
        pos_tags = pos_tag(words)
        return pos_tags

    def partOfSpeech(self, text):


        # Load the installed model
        nlp = spacy.load('en_core_web_sm')

        # Process a text
        doc = nlp(text)
        print([(w.text, w.pos_) for w in doc])  # Prints the text and the part of speech

        return doc
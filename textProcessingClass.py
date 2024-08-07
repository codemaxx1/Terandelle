

# imports
print("before importing spacy")
import spacy
import nltk
nltk.download('popular')  # This command downloads the most popular datasets and models


class TextProsessing:

    def partOfSpeech(self, text):


        # Load the installed model
        nlp = spacy.load('en_core_web_sm')

        # Process a text
        doc = nlp(text)
        print([(w.text, w.pos_) for w in doc])  # Prints the text and the part of speech

        return doc
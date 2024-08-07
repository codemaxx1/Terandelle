

# imports
import spacy
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag


'''
class for processing of text from user
'''
class TextProsessing:

    def update(self):
        nltk.download('popular')


    def analyzeCommand(self, command):
        nlp = spacy.load("en_core_web_sm")

        print(f"command to run (in analyzeCommand) {command}")

        commandAnalysis = nlp(command)
        # create list of all the sentances
        sentances = list(commandAnalysis.sent)

        for token in commandAnalysis:
            print(f"""TOKEN: {str(token)}=====TAG: {str(token.tag_):10} POS: {token.pos_}EXPLANATION: {spacy.explain(token.tag_)}""")

        return 1


    def preprocess(self, input_sentence):
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


    def recognize_intent(self, tokens):

        greeting_keywords = ['hello', 'hi', 'greetings', 'hey']
        tokens = [token.lower() for token, pos in tokens]
        if any(token in greeting_keywords for token in tokens):
            return "greeting"

        return "unknown"  # Default intent if no known intent is found


    def generate_response(self, intent):
        if intent == "greeting":
            return "Hello! How can I assist you today?"
        else:
            return "I am not sure how to respond to that. Can you please rephrase?"


    def chatbot(self, input_sentence):
        processed_input = self.preprocess(input_sentence)
        intent = self.recognize_intent(processed_input)
        response = self.generate_response(intent)
        return response
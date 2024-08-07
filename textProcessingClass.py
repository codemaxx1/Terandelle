

# imports
import spacy
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import os                                   #for directory scanning

# import custom tree
from binarySearchTree import Tree


'''
class for processing of text from user
'''
class TextProcessing:

    def __init__(self):
        # create tree of all identifying words
        self.WordTree = Tree()
        # get all keyword files
        path = os.getcwd() + "/keywords"
        dirList = os.listdir(path)
        print(f"Files and directories in {path} :")
        for file in dirList:
            print(f"file: {file}")
            with open(path + "/" + file, "r") as fileData:
                for word in fileData.readlines():
                    print(f"{file} contents: {word}")
                    # populate tree
                    self.WordTree.insert(word)


    def update(self):
        """
        update the nlp data
        :return:
        """
        nltk.download('popular')


    def analyzeCommand(self, command):
        nlp = spacy.load("en_core_web_sm")

        print(f"command to run (in analyzeCommand) {command}")

        # perform analysis of the command
        commandAnalysis = nlp(command)

        return commandAnalysis


    def recognizeIntent(self, command):
        # identify the important parts of speech from the command
        actions = []
        nouns = []
        properNouns = []

        for token in command:
            print(
                f"""TOKEN: {str(token)} \t\tTAG: {str(token.tag_)} \t POS: {token.pos_} \t EXPLANATION: {spacy.explain(token.tag_)}""")
            if str(token.tag_) == "VB":
                actions.append(token)
            if str(token.tag_) == "NN":
                nouns.append(token)
            if str(token.tag_) == "NNP":
                properNouns.append(token)
        print(f"actions to be performed: {actions}\nnouns captures: {nouns}\nproper noun captures: {properNouns}")


        """
        greeting_keywords = ['hello', 'hi', 'greetings', 'hey']
        tokens = [token.lower() for token, pos in tokens]
        if any(token in greeting_keywords for token in tokens):
            return "greeting"

        return "unknown"  # Default intent if no known intent is found
        """


    def partOfSpeech(self, text):
        # Load the installed model
        nlp = spacy.load('en_core_web_sm')

        # Process a text
        doc = nlp(text)
        print([(w.text, w.pos_) for w in doc])  # Prints the text and the part of speech

        return doc




    def chatbot(self, input_sentence):
        processed_input = self.preprocess(input_sentence)
        intent = self.recognize_intent(processed_input)
        response = self.generate_response(intent)
        return response
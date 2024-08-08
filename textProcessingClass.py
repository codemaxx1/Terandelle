

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
        self.listOfRelations = {}
        for file in dirList:
            print(f"file: {file}")
            with open(path + "/" + file, "r") as fileData:
                for word in fileData.readlines():
                    word = word.strip("\n")
                    word = word.strip(" ")
                    print(f"{file} contents: {word}")
                    # populate tree
                    #load relations into memory
                    self.listOfRelations.update({word : file})



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
        locatedFromFiles = []

        commandToRun = "unknownCommand"

        for token in command:
            print(f"""TOKEN: {str(token)} \t\tTAG: {str(token.tag_)} \t POS: {token.pos_} \t EXPLANATION: {spacy.explain(token.tag_)}""")
            if str(token.tag_) == "VB":
                actions.append(token)
            if str(token.tag_) == "NN":
                nouns.append(token)
            if str(token.tag_) == "NNP":
                properNouns.append(token)

            for word, reference in self.listOfRelations.items():
                if str(token) == str(word):
                    commandToRun = token
                    print(f"command to run is {token}")

        print(f"actions to be performed: {actions}\nnouns captures: {nouns}\nproper noun captures: {properNouns}")
        print(f"located from files -- {locatedFromFiles}")


        """
        greeting_keywords = ['hello', 'hi', 'greetings', 'hey']
        tokens = [token.lower() for token, pos in tokens]
        if any(token in greeting_keywords for token in tokens):
            return "greeting"

        return "unknown"  # Default intent if no known intent is found
        """

        return commandToRun

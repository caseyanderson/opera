from time import sleep
from datetime import datetime
from pathlib import Path
import os
import itertools

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import pos_tag

import argparse

class Opera:

    def __init__(self, filename):
        """ make a ghostses object
            read the corpus into object
        """
        self.filename = filename
        f = open(str(self.filename), 'r')
        self.corpus = f.read() # plaintext of the corpus


    def getSentences(self):
        """ tokenize corpus by sentence """
        self.sentences = sent_tokenize(score.corpus)        

    
    def getWords(self, preserveSpaces = True):
        """ tokenize corpus sentences by word """
        self.words = []
        for sentence in self.sentences:
            if preserveSpaces == True:
                words = [[word_tokenize(w), ' '] for w in sentence.split()]
                wordList = list(itertools.chain(*list(itertools.chain(*words))))
                if wordList[-1] == ' ':
                    # removes trailing whitespace @ end of sentence if there is any
                    wordList.pop()
                self.words.append(wordList)
            if preserveSpaces == False:
                words = word_tokenize(sentence)
                self.words.append(words)
        self.preserveSpaces = preserveSpaces
    
    def getPOS(self):
        """ parts of speech analysis
            TODO:
                1. if preserveSpaces
        """
        self.processedCorpus = []
        
        if self.preserveSpaces == False:
            print("removing spaces")
        elif self.preserveSpaces == True:
            # print("preserving spaces")
            sentenceStep = 0
            processedSentences = []
            for sentence in self.sentences:
                tokenizedSentence = word_tokenize(sentence)
                posSentence = pos_tag(tokenizedSentence)                
                processedSentence = []
                for word in self.words[sentenceStep]:
                    if word.isspace() == False:
                        posWord = list(posSentence.pop(0))
                        processedSentence.append([posWord[0], {"pos": posWord[1]}])
                    elif word.isspace() == True:
                        processedSentence.append(word)
                self.processedCorpus.append(processedSentence)
                sentenceStep+=1
                # print("~~~ no more words in sentence ~~~")
            # print("*** no more sentences in corpus ***")
            # print()

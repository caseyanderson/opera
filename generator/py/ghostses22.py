"""
ghostses22 (score generator) by Casey Anderson

6/21/22 by Casey Anderson

usage: python3 ghostses22.py --ws True

"""

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import pos_tag
from itertools import chain
from datetime import datetime
from pathlib import Path
from os import chdir, mkdir

import argparse

class Ghostses:
    
    def __init__(self, filename):
        """ make a score object, read the corpus into object """
        
        self.filename = filename
        f = open(str(self.filename), "r")
        self.corpus = f.read() # plaintext of the corpus
    
    
    def getSentences(self):
        """ tokenize corpus by sentence """
        self.sentences = sent_tokenize(self.corpus)        
    
    
    def getWords(self, preserveSpaces = True):
        """ tokenize sentences by word """
        
        self.words = []
        for sentence in self.sentences:
            if preserveSpaces == True:
                words = [[word_tokenize(w), " "] for w in sentence.split()]
                wordList = list(chain(*list(chain(*words))))
                if wordList[-1] == ' ':
                    # removes trailing whitespace @ end of sentence if there is any
                    wordList.pop()
                self.words.append(wordList)
            if preserveSpaces == False:
                words = word_tokenize(sentence)
                self.words.append(words)
        self.preserveSpaces = preserveSpaces
    
    
    def getTagsPOS(self):
        """ perform parts of speech analysis, store tags w/ words in processedCorpus """
        
        self.processedCorpus = []        
        if self.preserveSpaces == False:
            print("removing spaces")
        elif self.preserveSpaces == True:
            # print('preserving spaces')
            sentenceStep = 0
            processedSentences = []
            for sentence in self.sentences:
                tokenizedSentence = word_tokenize(sentence)
                posSentence = pos_tag(tokenizedSentence)                
                processedSentence = []
                for word in self.words[sentenceStep]:
                    if word.isspace() == False:
                        posWord = list(posSentence.pop(0))
                        processedSentence.append([posWord[0], {"tagPOS": posWord[1]}])
                    elif word.isspace() == True:
                        processedSentence.append(word)
                self.processedCorpus.append(processedSentence)
                sentenceStep+=1
    
    
    def categorizePOS(self, category, posSymbols):
        """ use parts of speech tags to group words into parts of speech categories """
        
        for symbol in posSymbols:
            sentenceCounter = 0
            for sentence in self.processedCorpus:
                wordCounter = 0
                for word in sentence:
                    if type(word) is list:
                        wordTagPOS = word[1].get("tagPOS")
                        if wordTagPOS == symbol:
                            self.processedCorpus[sentenceCounter][wordCounter][1]["categoryPOS"] = category
                    wordCounter+=1
                sentenceCounter+=1
    
    
    def styleCategoriesPOS4Layer(self, category):
        """ generate html tags for styling per category """
        
        for sentence in self.processedCorpus:
            for word in sentence:
                if type(word) is list:
                    categoryPOS = word[1].get("categoryPOS")
                    if categoryPOS == category:
                        taggedWord4Layer = "<span class='" + str(category) + "'>" + str(word[0]) + "</span>"
                    else:
                        taggedWord4Layer = "<span class='whitespace'>" + str(word[0]) + "</span>"
                    word[1].update({"styledPOS4Layer": taggedWord4Layer})
    
    
    def renderer(self, category):
        """ write styled text to html file per category """
        
        head = """
        <!DOCTYPE html>
        <html>
        <head>
        <link rel="stylesheet" href="../../css/styles.css" type="text/css"/>
        <link rel="stylesheet" href="../../css/print.css" media ="print" type="text/css"/>
        </head>
        <body>
        """
        body = ""
        foot = """
        </body>
        </html>
        """
        filename = category + ".html"
        o = open(filename, "w")
        for sentence in self.processedCorpus:
            for word in sentence:
                if type(word) is list:
                    body+=word[1].get("styledPOS4Layer")
                else:
                    body+=word[0]
        contents = head+body+foot
        o.write(contents)
        o.close()
    
    
    def proto(self):
        """ makes a prototyping directory, labeled stem-datetime
            changes directories into stem-datetime
        """
        
        thedir = "/home/cta/opera/generator/html"
        proto = datetime.now().strftime("%m%d%Y_%H%M%S")
        name = Path(self.filename).stem
        path = "".join([str(name), "-", str(proto)])
        chdir(thedir)
        try:
            mkdir(path)
        except OSError:
            print ("Creation of the directory %s failed" % path)
        else:
            print ("Successfully created the directory %s " % path)
        chdir(path)

def main():

    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--crps", type=str, default="/home/cta/opera/corpora/SteinGlazedNickel.txt",
                        help="the corpus")
    parser.add_argument("--ws", type=bool, default=False,
                        help="preserve whitespace")
    args = parser.parse_args()
    
    # setup
    score = Ghostses(args.crps)
    score.getSentences()
    score.getWords(preserveSpaces=args.ws)
    score.getTagsPOS()
    score.proto() # make the prototype dir
    
    # make the posKeysTags dictionary
    posKeysTags={}
    categories = ['noun', 'adjective', 'verb', 'adverb', 'background', 'symbol']
    tags = [
        ['NN','NNP','NNPS','NNS'],
        ['JJ','JJR','JJS'],
        ['VB','VBD','VBG','VBN','VBP','VBZ'],
        ['RB','RBR','RBS','WRB'],
        ['CC','CD','DT','EX','FW','IN','LS','MD','PDT','POS','PRP','PRP$','RP','TO','UH','WDT','WP','WP$'],
        ['$',"''",'(',')',',','--','.',':','SYM',"``"]
    ]

    for x, y in zip(categories, tags):
        posKeysTags[x] = y

    # make all of the layers, output to proto dir
    for category in categories:
        score.categorizePOS(category, posKeysTags[category])
        score.styleCategoriesPOS4Layer(category)
        score.renderer(category)

if __name__ == '__main__':
    main()
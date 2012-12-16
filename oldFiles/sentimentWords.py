#! /usr/bin/python
'''
Collects data from the sentiment lexicon text file, storing the data in 
a defaultdict.

Usage:
  data.keys()                    - all the words in the lexicon
  data[word]['<pos>']['polar']   - the polarity of the word
  data[word]['<pos']['type']     - the strength of the polarity
  data[word].keys()              - the POS tags of the given word
  data[word]['<pos>']['stemmed'] - whether or not the word is a stem
'''
#-----------------------------------------------------------------------------#
from collections import defaultdict
import re
#-----------------------------------------------------------------------------#
def getSentimentWords(filename):
  data = defaultdict(lambda: defaultdict(lambda: defaultdict(str)))
  
  infile = open(filename,'r')
  for line in infile:
    line = line.split()
    word = re.sub(r'^word1=','',line[2])
    pos  = re.sub(r'^pos1=','',line[3])    
    data[word][pos]['type'] = re.sub(r'^type=','',line[0])
    data[word][pos]['polar'] = re.sub(r'^priorpolarity=','',line[5])
    data[word][pos]['stemmed'] = re.sub(r'^stemmed1=','',line[4])
  
  return data
#-----------------------------------------------------------------------------#
if __name__ == '__main__':
  infile = 'sentimentLexicon.txt'
  data = getSentimentWords(infile)

  
  for word in data.keys():
    for pos in data[word].keys():
      print "data[%s][%s]['type'] = %s" %(word,pos,data[word][pos]['type'])
      print "data[%s][%s]['polar'] = %s" %(word,pos,data[word][pos]['polar'])
      print "data[%s][%s]['stemmed'] = %s" %(word,pos,data[word][pos]['stemmed'])
      print data[word].keys()
#-----------------------------------------------------------------------------#

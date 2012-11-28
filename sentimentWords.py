#! /usr/bin/python
'''
Collects data from the sentiment lexicom text file, storing the data in 
a defaultdict.

Usage:
  data[word]['polar']   - the polarity of the word
  data[word]['type']    - the strength of the polarity
  data[word]['pos']     - the POS tag of the given word
  data[word]['stem']    - whether or not the word is a stem
'''
#-----------------------------------------------------------------------------#
from collections import defaultdict
import re
#-----------------------------------------------------------------------------#
def getSentimentWords(filename):
  data = defaultdict(lambda: defaultdict(str))
  
  infile = open(filename,'r')
  for line in infile:
    line = line.split()
    word = re.sub(r'^word1=','',line[2])
    data[word]['type'] = re.sub(r'^type=','',line[0])
    data[word]['polar'] = re.sub(r'^priorpolarity=','',line[5])
    data[word]['pos'] = re.sub(r'^pos1=','',line[3])
    data[word]['stemmed'] = re.sub(r'^stemmed1=','',line[4])
  
  return data
#-----------------------------------------------------------------------------#
if __name__ == '__main__':
  infile = 'sentimentLexicon.txt'
  data = getSentimentWords(infile)

  '''
  for word in data.keys():
    print 'word:%15s\tpolarity: %8s\ttype: %11s\tpos: %s' \
        %(word,data[word]['polar'],data[word]['type'],data[word]['pos'])
  '''
#-----------------------------------------------------------------------------#

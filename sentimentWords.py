from collections import defaultdict
import re

def getSentimentWords(filename):
  data = defaultdict(lambda: defaultdict(str))
  
  infile = open(filename,'r')
  for line in infile:
    line = line.split()
    word = re.sub(r'^word1=','',line[2])
    data[word]['type'] = re.sub(r'^type=','',line[0])
    data[word]['polar'] = re.sub(r'^priorpolarity=','',line[5])
    data[word]['pos'] = re.sub(r'^pos1=','',line[3])
  
  return data

if __name__ == '__main__':
  infile = 'sentimentLexicon.txt'
  data = getSentimentWords(infile)
  #for word in data.keys():
    #print word, data[word]['type'],data[word]['polar'],data[word]['pos']

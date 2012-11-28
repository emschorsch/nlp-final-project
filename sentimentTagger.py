#! /usr/bin/python
"""
Implements a sentiment analyzer. The analyzer trains on annotated tweets.
A few different methods are implemented to identify the sentiment of a new 
tweet.
1) A simple count of the number of sentiment types
2) something complicated
"""
from collections import defaultdict
from sentimentWords import getSentimentWords

#some global values
TRAINFILE = 'outputTestA.txt'
POLAR = 4 #the index of the polarity
TWEET = 5 #the index of the tweet itself

"""
builds a list of the data based on the info in filename
"""
def extractData( fileName ):
  #build the list of test words
  f = open(TRAINFILE, 'r')
  trainData = map(lambda f: f.strip('\n').split('\t'), f.readlines())
  f.close()
  return trainData


def useSentimentWordsOnly(sentimentWords,trainData):
  taggedData = []
  for instance in trainData:
    tweet = instance[TWEET]
    strongNeg = weakNeg = strongPos = weakPos = 0
    for word.strip('!@#$%^&*(),.?\"') in tweet:
      
      # counts the number of pos and neg words in the tweet
      if sentimentWords[word]['polar'] == 'negative':
	strongNeg += 1
      elif sentimentWords[word]['polar'] == 'positve':
        strongPos += 1

      # checks if the majority of words are pos or neg
      if strongPos == strongNeg:
	taggedData.append('neutral')
      elif strongPos > strongNeg:
	taggedData.append('positive')
      else:
	taggedData.append('negative')
  return taggedData


def main():
  trainData = extractData( TRAINFILE )
  print trainData[0]
  sentimentWords = getSentimentWords('sentimentLexicon.txt')
  taggedData = useSentimentWordsOnly(sentimentWords, trainData)
  # checkData(taggedData,trainData)
  print taggedData


if __name__=='__main__':
  main()


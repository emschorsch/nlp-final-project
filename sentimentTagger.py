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
from decision import *
from random import *

#some global values
TRAINFILE = 'outputTestA.txt'
POLAR = 4 #the index of the polarity
TWEET = 5 #the index of the tweet itself

"""
builds a list of the data based on the info in filename
"""
def extractData( fileName ):
  #builds the list of test words
  f = open(TRAINFILE, 'r')
  #lines = filter(lambda x: "Not Available" not in x, f.readlines()) 
  trainData = map(lambda x: x.strip('\n').split('\t'), f.readlines())
  f.close()
  return trainData

"""
Returns a dict of counts of sense per feature, and total #of sense
"""
def featureCounts( data ):
  featCounts = {}
  senseTotals = {}
  for line in data:
    print line
    start = int(line[2])
    end = int(line[3])
    for feat in line[TWEET].split()[start:end]: #+1 counts for words in range
      if feat in featCounts:
        featCounts[feat][line[POLAR]] = featCounts[feat].get(line[POLAR], 0) +1
        senseTotals[line[POLAR]] = senseTotals.get(line[POLAR], 0) + 1
      else:
        featCounts[feat] = { line[POLAR] : 1 }
  return featCounts, senseTotals

"""
Returns a dict of probabilities: P(f_i | s) where keys are (f_i, s) tuples
"""
def buildFeaturesProb( data ):
  probDict = {}
  featCounts, senseTotals = featureCounts( data )
  for feat in featureCounts.keys():
    for sentim in featureCounts[feat].keys():
      prob = featCounts[feat][sentim] / float( senseTotals[sentim] )
      probDict[(feat, sentim)] = prob
  total = sum(senseTotals.values())
  for sentim in senseTotals.keys():
    probDict[sentim] = senseTotals[sentim]/total
  return probDict

"""
Returns the best guess for the "correct" sense using the naive bayes algo
"""
def naiveProb( data, features ):
  probDict = buildFeaturesProb( data )
  probList = []
  for sense in sentiments:
    p = 1*probDict[sentim] #multiplying prob by P(s)
    for feat in features:
      p*= probDict[(feat, sense)]
    probList.append( p, sense )
  probList.sort() #defaults to sorting on the first element
  return probList[0]


def main():
  trainData = extractData( TRAINFILE )
  sentimentWords = getSentimentWords('sentimentLexicon.txt')
  taggedData = useSentimentWordsOnly(sentimentWords, trainData)
  print trainData
  checkData(taggedData,trainData)
  probDict = buildFeaturesProb( trainData )
  
if __name__=='__main__':
  main()

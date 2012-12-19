#! /usr/bin/python
"""
Implements a sentiment analyzer. The analyzer trains on annotated tweets.
A few different methods are implemented to identify the sentiment of a new 
tweet.
1) A simple count of the number of sentiment types
2) something complicated
"""
from collections import defaultdict
#from decision import *
from random import *
from checkTags import checkListTags
import sys

#some global values
TRAINFILEA = 'trainA.txt'
TRAINFILEB = 'trainB.txt'
POLARA = 4 #the index of the polarity
POLARB = 3 #index of polarity in task B
TWEETA = 5 #the index of the tweet itself
TWEETB = 4 #index of twee in task B

"""
builds a list of the data based on the info in filename
"""
def extractData( fileName ):
  #builds the list of test words
  f = open( fileName, 'r')
  #lines = filter(lambda x: "Not Available" not in x, f.readlines()) 
  trainData = map(lambda x: x.strip('\n').split('\t'), f.readlines())
  f.close()
  return trainData

"""
returns a list of all the n-grams in the text
"""
def ngramList( text, n ):
  ngrams = []
  words = text.split()
  for i in xrange(0,len(words) - n + 1):
    ngrams.append(" ".join(words[i:i+n]))
  return ngrams

"""
returns a list of all the n-grams up to k in the text
"""
def allGrams( text, k):
  ngrams = []
  for i in xrange(1,k+1):
    ngrams.extend(ngramList( text, i ))
  return ngrams

"""
Returns a dict of counts of sense per feature, and total #of sense, for taskA
"""
def featureCountsA( data, n ):
  featCounts = {}
  senseTotals = {}
  for line in data:
    start = int(line[2])
    end = int(line[3]) + 1
    text = " ".join( line[TWEETA].split()[start:end] )
    for feat in allGrams( text, n ): #+1 counts for words in range
      if feat in featCounts:
        featCounts[feat][line[POLARA]] = featCounts[feat].get(line[POLARA],0)+1
        senseTotals[line[POLARA]] = senseTotals.get(line[POLARA], 0) + 1
      else:
        featCounts[feat] = { line[POLARA] : 1 }
  return featCounts, senseTotals

"""
Returns a dict of counts of sense per feature, and total #of sense, for taskA
"""
def featureCountsB( data, n ):
  featCounts = {}
  senseTotals = {}
  for line in data:
    for feat in allGrams( line[TWEETB], n ): #+1 counts for words in range
      if feat in featCounts:
        featCounts[feat][line[POLARB]] = featCounts[feat].get(line[POLARB],0)+1
        senseTotals[line[POLARB]] = senseTotals.get(line[POLARB], 0) + 1
      else:
        featCounts[feat] = { line[POLARB] : 1 }
  return featCounts, senseTotals

"""
Returns a dict of probabilities: P(f_i | s) where keys are (f_i, s) tuples
"""
def buildFeaturesProb( data, taskA, n ):
  probDict = {}
  if taskA == True:
    featCounts, senseTotals = featureCountsA( data, n )
  else:
    featCounts, senseTotals = featureCountsB( data, n )
  for feat in featCounts.keys():
    for sentim in featCounts[feat].keys():
    #for sentim in senseTotals.keys():
      v = len(featCounts[feat].keys())
      #print len(featCounts[feat].keys())
      prob = ( featCounts[feat].get( sentim, 0) + 1 ) / \
        float( senseTotals[sentim] + 1 )
      probDict[(feat, sentim)] = prob
  total = sum(senseTotals.values())
  for sentim in senseTotals.keys():
    probDict[sentim] = senseTotals[sentim]/float( total )
  return senseTotals.keys(), probDict

"""
Returns the best guess for the "correct" sense using the naive bayes algo
"""
def naiveProb( features, probDict, sentiments ):
  probList = []
  for sense in sentiments:
    #p = 1.0 * probDict[sense]
    ""
    if probDict[sense] > .5:
      p = 1.0
    else:
      p = 2.0 #*probDict[sense] #multiplying prob by P(s)
      ""
    for feat in features:
      p *= probDict.get( (feat, sense), .5)
    probList.append( (p, sense) )
  probList.sort() #defaults to sorting on the first element in tuple
  return probList[0]

"""
Returns the best guess for each tweet segment
"""
def naiveBayes( train, test, n, task = True ):
  if task == True:
    sentim, probDict = buildFeaturesProb( train, task, n )
  else:
    sentim, probDict = buildFeaturesProb( train, task, n )
  tags = []
  for line in test:
    if task == True:
      start = int(line[2])
      end = int(line[3]) + 1
      text = " ".join( line[TWEETA].split()[start:end] )
      tag = naiveProb( allGrams(text , n), probDict, sentim )
    else:
      tag = naiveProb( allGrams(line[TWEETB], n), probDict, sentim )
    tags.append(tag)
  return tags

"""
splits train data
"""
def crossValid( trainFrac, trainData):
  lines = len(trainData)
  end = int(lines*trainFrac)
  train = trainData[0:end]
  test = trainData[int(.8*lines):lines]
  return train, test


def main():
  task = True
  fileName = TRAINFILEA
  if len(sys.argv) > 1:
    task = sys.argv[1]
    if task.lower() == "a":
      task = True
      fileName = TRAINFILEA
    else:
      task = False
      fileName = TRAINFILEB
  trainFile = extractData( fileName )
  trainData, testData = crossValid(.8, trainFile)
  #sentimentWords = getSentimentWords('sentimentLexicon.txt')
  #checkData(taggedData,trainData)
  tags = naiveBayes( trainData, testData, 3, task )
  checkListTags(tags, testData, task)
  
if __name__=='__main__':
  main()

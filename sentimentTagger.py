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

"""
blah
"""
def useSentimentWordsOnly(sentimentWords,trainData):
  taggedData = []
  for instance in trainData:
    if len(instance) == 6:
      tweet = instance[TWEET]
      neg = pos = 0
      
      for word in tweet.split():
        word = word.strip('!@#$%^&*(),.?\"') 
   
        # counts the number of pos and neg words in the tweet
        if sentimentWords[word]['polar'] == 'negative':
          neg += 1
        elif sentimentWords[word]['polar'] == 'positve':
          pos += 1

      # checks if the majority of words are pos or neg
      if pos == neg:
	if random() > .5:
          taggedData.append('positive')
        else:
          taggedData.append('negative')
      elif pos > neg:
        taggedData.append('positive')
      else:
       taggedData.append('negative')

  return taggedData

def checkData(taggedData,trainData):
  count = correct =  0
  for instance in trainData:
    if len(instance) == 6:
      tag = taggedData[count]
      if tag == instance[POLAR]:
        correct += 1
      count += 1
  print 'Percent Correct: %f (%d/%d)' %(float(correct)/count,correct,count)
     
def useRules(trainDataB,rules):
  taggedData = []
  for ID in trainDataB.keys():
    currentTweet = trainDataB[ID]['tweet']
    pos = neg = neut = 0
    for word in currentTweet.split():
      #print type(rules[word]['tag'])
      if rules[word]['tag'] == "positive":
        print word
        pos += 1
      elif rules[word]['tag'] == "negative":
        neg += 1
      else:
        neut += 1
 
    if pos > neg and pos > neut:
      taggedData.append("positive")
    elif neg > pos and neg > neut: 
      taggedData.append('negative')
    else:
      taggedData.append('neutral')

  return taggedData

def checkDataB(taggedData,trainDataB):
  correct = count = 0
  for key in trainDataB.keys():
    correctTag = trainDataB[key]['tag']
    if correctTag == taggedData[count]:
      correct += 1
    count += 1 
  print 'Percent Correct: %f (%d/%d)' %(float(correct)/count,correct,count)

def main():
  trainData = extractData( TRAINFILE )
  sentimentWords = getSentimentWords('sentimentLexicon.txt')
  taggedData = useSentimentWordsOnly(sentimentWords, trainData)
  print trainData
  checkData(taggedData,trainData)
  probDict = buildFeaturesProb( trainData )
  
  # using decision
  trainingFileA = 'outputTestA.txt'
  trainingFileB = 'outputTestB.txt'
  trainDataA = parseA(trainingFileA)
  trainDataB = parseB(trainingFileB)
  rules = train(trainDataA,trainDataB)
  taggedData = useRules(trainDataB,rules)
  checkDataB(taggedData,trainDataB)

if __name__=='__main__':
  main()

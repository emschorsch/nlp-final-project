'''
'''
from decisionParse import parseA, parseB
from collections import defaultdict
from random import *
from math import *
import operator

def train(trainDataA,trainDataB):

  # a of rules containing a word and its tag for the decision list
  rules = defaultdict(lambda: defaultdict(str))

  # a list of word counts for the decision list
  wordCounts = defaultdict(lambda: defaultdict(int))

  # a list of words to ignore
  ignoreWords = ['the','be','to','of','and','a','in','that','have','i','it','for','not','on','with']

  for dataID in trainDataB.keys():

    # data involving the current twitter message
    currentTweetData = trainDataB[dataID]
    currentTag = currentTweetData['tag']
    currentTweet = currentTweetData['tweet'].split()
    
    for word in currentTweet:
       word = word.lower().strip('.,?@!\"\'#*:')
       if word not in ignoreWords:
         wordCounts[word][currentTag] += 1
  
  for word in wordCounts.keys():
    currentMax = 0
    maxString = ''
    for tag in wordCounts[word].keys():
      if wordCounts[word][tag] > currentMax:
        currentMax = wordCounts[word][tag]
        maxString = tag
    rules[word]['tag'] = maxString
    rules[word]['count'] = currentMax
      
  return rules
      
if __name__ == '__main__':
  trainingFileA = 'outputTestA.txt'
  trainingFileB = 'outputTestB.txt'
  trainDataA = parseA(trainingFileA)
  trainDataB = parseB(trainingFileB)
  train(trainDataA,trainDataB)

#!/usr/bin/python

from dataParse import parseB, parseA
from collections import defaultdict
from checkTags import checkTagsA, checkTagsB
from random import *
import re

# ----------------------------------------------------------------- #

def lexiconTag(trainA, trainB, lexicon):
  '''
  Takes in two sources of data (for A and B) and then generates tags
  based on the number of weighted words containged within each tweet
  '''

  # Dictionary of tags - usage: tags[ID][index] = tag  
  tagsA = defaultdict(lambda: defaultdict(str))
  tagsB = defaultdict(lambda: defaultdict(str))

  # Use Lexicon to tag data from trainA
  for ID in trainA.keys():
    for index in trainA[ID].keys():
      start,end = index
      tweet = (trainA[ID][index]['tweet']).split()[int(start):int(end)]
      pos = neg = 0
      for word in tweet:
        word = word.lower().strip("-=+(),!@#$%^&*./\"\'")

	# determine the number of weighted words in the tweet
        for position in lexicon[word].keys():
          if lexicon[word][position]['polar'] == 'positive':
            pos += 1
          elif lexicon[word][position]['polar'] == 'negative':
            neg += 1
	
      # tag the tweet
      if pos > neg:
        tagsA[ID][index] = 'positive'
      elif pos < neg: 
        tagsA[ID][index] = 'negative'
      else:
        tagsA[ID][index] = choice(['objective'])
   
  # Use Lexicon to tag data from trainB
  for ID in trainB.keys():
    for subject in trainB[ID].keys():
      tweet = (trainB[ID][subject]['tweet']).split()
      pos = neg = 0
      for word in tweet:
        word = word.lower().strip(",!@#$%^&*./\"\'")

	# determine the number of weighted words in the tweet
        for position in lexicon[word].keys():
          if lexicon[word][position]['polar'] == 'positive':
            pos += 1
          elif lexicon[word][position]['polar'] == 'negative':
            neg += 1

      # tag the tweet
      if pos > neg:
        tagsB[ID][subject] = 'positive'
      elif pos < neg: 
        tagsB[ID][subject] = 'negative'
      else:
        tagsB[ID][subject] = choice(['objective'])
  
  return tagsA, tagsB


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

# ----------------------------------------------------------------- #

def weightedRandomTag(train, test, task):
  '''
  Takes in two sources of data (test and train for a) and then 
  genterates tags based on the frequency of the tags found in 
  the test data and applies them to the train data
  '''

  # Get counts for trainA
  posC = negC = neutC = objC = totalC = 0.0
  for ID in train.keys():
    for index in train[ID].keys():
      if train[ID][index]['polar'] == 'positive':  posC  += 1
      if train[ID][index]['polar'] == 'negative':  negC  += 1
      if train[ID][index]['polar'] == 'neutral':   neutC += 1
      if train[ID][index]['polar'] == 'objective': objC  += 1
      totalC += 1
  
  #print '\tCounts: Pos: %.0f Neg: %.0f Neut: %.0f Obj: %.0f' \
      #%(posC, negC, neutC, objC)

  # Get percents for train
  posP  = posC/totalC
  negP  = negC/totalC
  neutP = neutC/totalC
  objP  = objC/totalC
  
  # Use percents to randomly tag words and check correctness of tag
  correct = 0.0
  total = 0.0
  for ID in test.keys():
    for index in test[ID].keys():
      currentPolar = test[ID][index]['polar']
      percent = random()
      if percent > (1 - objP): guess = 'objective'
      elif percent > (1 - posP - negP): guess = 'negative'
      elif percent > (1 - posP - negP - neutP): guess = 'neutral'
      else: guess = 'positive'
      if currentPolar == guess:
        correct += 1
      total += 1

  print '[Task %s] Percent Correct:  %f (%.0f/%.0f)' \
      %(task, correct/total, correct, total)

# ----------------------------------------------------------------- #

def mfsTag(train,test,task):
  pos = neg = obj = neut = 0
  correct = total = 0.0
  for ID in train.keys():
    for index in train[ID].keys():
      if train[ID][index]['polar'] == 'positive':  pos  += 1
      if train[ID][index]['polar'] == 'negative':  neg  += 1
      if train[ID][index]['polar'] == 'neutral':   neut += 1
      if train[ID][index]['polar'] == 'objective': obj  += 1
  
  if pos > neg and pos > neut and pos > obj: mfs = 'positive'
  elif neg > pos and neg > neut and neg > obj: mfs = 'negative'
  elif neut > neg and neut > pos and neut > obj: mfs = 'neutral'
  elif obj > neg and obj > neut and obj > pos: mfs = 'objective'
  
  for ID in test.keys():
    for index in test[ID].keys():
      if test[ID][index]['polar'] == mfs:
        correct += 1
      total += 1
  print correct,total
  print '[Task %s] Most Frequent (%s): Percent Correct:  %0.4f (%.0f/%.0f)' \
      %(task, mfs, correct/total, correct, total)

# ----------------------------------------------------------------- #

def trueRandom(train, test, task):
  correct = total = 0.0
  polars = ['positive','negative','neutral','objective']
  for ID in test.keys():
    for index in test[ID].keys():
      randomChoice = choice(polars)
      if randomChoice == test[ID][index]['polar']: 
        correct += 1
      total += 1

  print '[Tast %s] Percent Correct:  %.2f (%.0f/%.0f)' \
      %(task, correct/total, correct, total)

# ----------------------------------------------------------------- #

if __name__ == '__main__':

  # file names
  trainingFileA = 'trainA.txt'
  trainingFileB = 'trainB.txt'
  lexiconFile   = 'sentimentLexicon.txt'

  # parse training and testing data
  trainA, testA  = parseA(trainingFileA,5)
  trainB, testB  = parseB(trainingFileB,5)
  lexicon = getSentimentWords(lexiconFile)

  # mfs tagging
  print '\nMOST FREQUENT SENSE'
  mfsTag(trainA, testA, 'A')
  mfsTag(trainB, testB, 'B')

  # lexicon tagger
  print '\nLEXICON TAGGER'
  tagsA, tagsB = lexiconTag(testA, testB, lexicon)
  checkTagsA(tagsA,testA)
  checkTagsB(tagsB,testB)

  # random tagging
  #print '\nRANDOM'
  #trueRandom(trainA, testA, 'A')
  #trueRandom(trainB, testB, 'B')

  # weighted random
  #print '\nWEIGHTED RANDOM'
  #weightedRandomTag(trainA, testA, 'A')  
  #weightedRandomTag(trainB, testB, 'B')

# ----------------------------------------------------------------- #

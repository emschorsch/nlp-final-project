from dataParse import parseA, parseB
from sentimentWords import getSentimentWords
from collections import defaultdict
from random import *

# ----------------------------------------------------------------- #
def weightedRandomTag(train, test):
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
  
  print '\tCounts: Pos: %.0f Neg: %.0f Neut: %.0f Obj: %.0f' \
      %(posC, negC, neutC, objC)

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

  print '\tWeighted Random: Percent Correct:  %f (%.0f/%.0f)' \
      %(correct/total, correct, total)
# ----------------------------------------------------------------- #

def mfsTag(train,test):
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

  print '\tMost Frequent (%s): Percent Correct:  %f (%.0f/%.0f)' \
      %(mfs, correct/total, correct, total)

# ----------------------------------------------------------------- #

def trueRandom(train, test):
  correct = total = 0.0
  polars = ['positive','negative','neutral','objective']
  for ID in test.keys():
    for index in test[ID].keys():
      randomChoice = choice(polars)
      if randomChoice == test[ID][index]['polar']: 
        correct += 1
      total += 1

  print '\tRandom: Percent Correct:  %f (%.0f/%.0f)' \
      %(correct/total, correct, total)

# ----------------------------------------------------------------- #

if __name__ == '__main__':
  trainingFileA = 'trainA.txt'
  trainingFileB = 'trainB.txt'
  trainA, testA = parseA(trainingFileA)
  trainB, testB = parseB(trainingFileB)
  print "[TASK A]"
  weightedRandomTag(trainA, testA)
  mfsTag(trainA, testA)
  trueRandom(trainA, testA)
  print "[TASK B]"
  weightedRandomTag(trainB, testB)
  mfsTag(trainB, testB)
  trueRandom(trainB, testB)

# ----------------------------------------------------------------- #

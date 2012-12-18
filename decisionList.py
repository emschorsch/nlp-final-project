#!/usr/bin/python
from math import log
from dataParse import parseA, parseB
from collections import defaultdict
from operator import itemgetter
from checkTags import checkTagsB, checkTagsA
# ----------------------------------------------------------------- #

def getScores(scores,mfp):
  alpha = 1
  for word in mfp.keys():
    wordScores = []
    total = mfp[word]['count']
    for polar in mfp[word].keys():
      if polar != 'count':
        count = mfp[word][polar]
        score = log((count+alpha)/(float(total-count)+alpha))
        wordScores.append((word,polar,score))
    
    topScore = sorted(wordScores, key=itemgetter(2), reverse=True)[0]
    scores[word]['polar'] = topScore[1]
    scores[word]['score'] = topScore[2]  

# ----------------------------------------------------------------- #

def getTags(rules,test,mfs):
  
  tags = defaultdict(lambda: defaultdict(str))
  pos = neg = obj = neut = 0  

  for ID in test.keys():
    for index in test[ID].keys():
      currentTweet = test[ID][index]['tweet'].split()
      editedTweet = []
      for word in currentTweet:
        editedTweet.append(word.lower().strip('\'\"!@#$%^&*(),.?<>;:-'))
      ' '.join(editedTweet)
      taggedFlag = False
      for ruleSet in rules:
        rule, polar, score = ruleSet[0], ruleSet[1], ruleSet[2]
        if rule in editedTweet and score > 0:
          tags[ID][index] = polar
          taggedFlag = True
          break
      if not taggedFlag:
        tags[ID][index] = mfs
  return tags

# ----------------------------------------------------------------- #

def getUnigrams(train):
  mfp = defaultdict(lambda: defaultdict(int))
  pos = neg = obj = neut = 0

  for ID in train.keys():
    for subj in train[ID].keys():
      if train[ID][subj]['polar'] == 'positive':  pos  += 1
      if train[ID][subj]['polar'] == 'negative':  neg  += 1
      if train[ID][subj]['polar'] == 'neutral':   neut += 1
      if train[ID][subj]['polar'] == 'objective': obj  += 1
      tweet = train[ID][subj]['tweet'].split()
      for word in tweet:
        word1 = word.lower().strip('\'\"!@#$%^&*(),.?<>;:-')
        polar = train[ID][subj]['polar']
        mfp[word1][polar] += 1
        mfp[word1]['count'] += 1
  
  if pos > neg and pos > neut and pos > obj: mfs = 'positive'
  elif neg > pos and neg > neut and neg > obj: mfs = 'negative'
  elif neut > neg and neut > pos and neut > obj: mfs = 'neutral'
  elif obj > neg and obj > neut and obj > pos: mfs = 'objective'
  return mfp, mfs

# ----------------------------------------------------------------- #

def getBigrams(train):
  mfp = defaultdict(lambda: defaultdict(int))  
  pos = neg = obj = neut = 0
  
  for ID in train.keys():
    for subj in train[ID].keys():
      if train[ID][subj]['polar'] == 'positive':  pos  += 1
      if train[ID][subj]['polar'] == 'negative':  neg  += 1
      if train[ID][subj]['polar'] == 'neutral':   neut += 1
      if train[ID][subj]['polar'] == 'objective': obj  += 1
      tweet = train[ID][subj]['tweet'].split()
      for i in range(1,len(tweet)):
        w1 = tweet[i-1].lower().strip('\'\"!@#$%^&*(),.?<>;:')
	w2 = tweet[i].lower().strip('\'\"!@#$%^&*(),.?<>;:')
        bigram = w1 + ' ' + w2
        polar = train[ID][subj]['polar']
        mfp[bigram][polar] += 1
        mfp[bigram]['count'] += 1

  if pos > neg and pos > neut and pos > obj: mfs = 'positive'
  elif neg > pos and neg > neut and neg > obj: mfs = 'negative'
  elif neut > neg and neut > pos and neut > obj: mfs = 'neutral'
  elif obj > neg and obj > neut and obj > pos: mfs = 'objective'
  return mfp, mfs

def getTrigrams(train):
  mfp = defaultdict(lambda: defaultdict(int))  
  pos = neg = obj = neut = 0
  
  for ID in train.keys():
    for subj in train[ID].keys():
      if train[ID][subj]['polar'] == 'positive':  pos  += 1
      if train[ID][subj]['polar'] == 'negative':  neg  += 1
      if train[ID][subj]['polar'] == 'neutral':   neut += 1
      if train[ID][subj]['polar'] == 'objective': obj  += 1
      tweet = train[ID][subj]['tweet'].split()
      for i in range(2,len(tweet)):
        w1 = tweet[i-1].lower().strip('\'\"!@#$%^&*(),.?<>;:')
	w2 = tweet[i].lower().strip('\'\"!@#$%^&*(),.?<>;:')
        w3 = tweet[i-2].lower().strip('\'\"!@#$%^&*(),.?<>;:')
        trigram = w3 + ' ' + w1 + ' ' + w2
        polar = train[ID][subj]['polar']
        mfp[trigram][polar] += 1
        mfp[trigram]['count'] += 1

  if pos > neg and pos > neut and pos > obj: mfs = 'positive'
  elif neg > pos and neg > neut and neg > obj: mfs = 'negative'
  elif neut > neg and neut > pos and neut > obj: mfs = 'neutral'
  elif obj > neg and obj > neut and obj > pos: mfs = 'objective'
  return mfp, mfs

# ----------------------------------------------------------------- #

def unigramsBigrams(train):
  mfp = defaultdict(lambda: defaultdict(int))  
  pos = neg = obj = neut = 0
  
  for ID in train.keys():
    for subj in train[ID].keys():
      if train[ID][subj]['polar'] == 'positive':  pos  += 1
      if train[ID][subj]['polar'] == 'negative':  neg  += 1
      if train[ID][subj]['polar'] == 'neutral':   neut += 1
      if train[ID][subj]['polar'] == 'objective': obj  += 1
      tweet = train[ID][subj]['tweet'].split()
      for i in range(1,len(tweet)):
        w1 = tweet[i-1].lower().strip('\'\"!@#$%^&*(),.?<>;:')
	w2 = tweet[i].lower().strip('\'\"!@#$%^&*(),.?<>;:')
        bigram = w1 + ' ' + w2
        polar = train[ID][subj]['polar']
        mfp[bigram][polar] += 1
        mfp[bigram]['count'] += 1
      for word in tweet:
        word1 = word.lower().strip('\'\"!@#$%^&*(),.?<>;:-')
        polar = train[ID][subj]['polar']
        mfp[word1][polar] += 1
        mfp[word1]['count'] += 1

  if pos > neg and pos > neut and pos > obj: mfs = 'positive'
  elif neg > pos and neg > neut and neg > obj: mfs = 'negative'
  elif neut > neg and neut > pos and neut > obj: mfs = 'neutral'
  elif obj > neg and obj > neut and obj > pos: mfs = 'objective'
  return mfp, mfs


# ----------------------------------------------------------------- #

def decisionList(train,test):
  scores = defaultdict(lambda: defaultdict(int))

  # get counts of the mfp (most frequent polarity)
  #mfp, mfs = getUnigrams(train)
  mfp, mfs = getBigrams(train)
  #mfp, mfs = getTrigrams(train)
  #mfp, mfs = unigramsBigrams(train)
  
  # get the highest score for each unigram and its associated polarity
  getScores(scores,mfp)
  scoresSort = []
  for word in scores.keys():
    scoresSort.append((word, scores[word]['polar'], scores[word]['score']))
  scoresSort = sorted(scoresSort, key=itemgetter(2), reverse = True)
  
  #for item in scoresSort[:50]:
    #print "Word: %20s  Polar: %10s Score:%0.2f" %(item[0],item[1],item[2])

  tags = getTags(scoresSort,test,mfs)
  return tags
  
# ----------------------------------------------------------------- #      

if __name__ == '__main__':
  # file names
  trainingFileA = 'trainA.txt'
  trainingFileB = 'trainB.txt'

  # parse training and testing data
  trainA, testA  = parseA(trainingFileA)
  trainB, testB  = parseB(trainingFileB)
  
  # decision list
  print '\nDECISION LIST'
  tagsA = decisionList(trainA,testA)
  tagsB = decisionList(trainB,testB)
  checkTagsA(tagsA,testA)
  checkTagsB(tagsB,testB)

# ----------------------------------------------------------------- #

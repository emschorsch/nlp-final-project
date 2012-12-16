#!/usr/bin/python
from math import log
from dataParse import parseA, parseB
from collections import defaultdict
from operator import itemgetter
from checkTags import checkTagsB
TWEET = 5
# ----------------------------------------------------------------- #

def getScores(scores,mfp):
  alpha = 0.1
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

def getTags(rules,test):
  
  '''
  total = correct = 0.0
  for ID in test.keys():
    for index in test[ID].keys():
      currentPolar = test[ID][index]['polar']
      currentTweet = test[ID][index]['tweet']
      for ruleSet in rules:
        rule,polar,score = ruleSet[0],ruleSet[1],ruleSet[2]
        if rule in currentTweet and score > 0:
          if polar ==  currentPolar: 
            correct += 1
            break
        else:
          if 'positive' == currentPolar: 
            correct += 1
            break
      total += 1
  print '\tDecision List: Percent Correct:  %f (%.0f/%.0f)' \
      %(correct/total, correct, total)
  '''
  tags = defaultdict(lambda: defaultdict(str))
  
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
        tags[ID][index] = 'positive'
  return tags

# ----------------------------------------------------------------- #

def getUnigrams(train):
  mfp = defaultdict(lambda: defaultdict(int))  
  for ID in train.keys():
    for subj in train[ID].keys():
      tweet = train[ID][subj]['tweet'].split()
      for word in tweet:
        word1 = word.lower().strip('\'\"!@#$%^&*(),.?<>;:-')
        polar = train[ID][subj]['polar']
        mfp[word1][polar] += 1
        mfp[word1]['count'] += 1
  return mfp

# ----------------------------------------------------------------- #

def getBigrams(train):
  mfp = defaultdict(lambda: defaultdict(int))  
  for ID in train.keys():
    for subj in train[ID].keys():
      tweet = train[ID][subj]['tweet'].split()
      for i in range(1,len(tweet)):
        w1 = tweet[i-1].lower().strip('\'\"!@#$%^&*(),.?<>;:')
	w2 = tweet[i].lower().strip('\'\"!@#$%^&*(),.?<>;:')
        bigram = w1 + ' ' + w2
        polar = train[ID][subj]['polar']
        mfp[bigram][polar] += 1
        mfp[bigram]['count'] += 1
  return mfp

# ----------------------------------------------------------------- #

def unigramsBigrams(train):
  mfp = defaultdict(lambda: defaultdict(int))  
  for ID in train.keys():
    for subj in train[ID].keys():
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
  return mfp


# ----------------------------------------------------------------- #

def decisionList(train,test):
  scores = defaultdict(lambda: defaultdict(int))

  # get counts of the mfp (most frequent polarity)
  mfp = getUnigrams(train)
  #mfp = getBigrams(train)
  #mfp = unigramsBigrams(train)
  
  # get the highest score for each unigram and its associated polarity
  getScores(scores,mfp)
  scoresSort = []
  for word in scores.keys():
    scoresSort.append((word, scores[word]['polar'], scores[word]['score']))
  scoresSort = sorted(scoresSort, key=itemgetter(2), reverse = True)
  
  for item in scoresSort[:50]:
    print "Word: %20s  Polar: %10s Score:%0.2f" %(item[0],item[1],item[2])

  tags = getTags(scoresSort,test)
  return tags
  
# ----------------------------------------------------------------- #      

if __name__ == '__main__':
  trainingFile = 'trainA.txt'
  train, test = parseA(trainingFile)
  tags = decisionList(train,test)
  checkTagsB(tags,test)

# ----------------------------------------------------------------- #

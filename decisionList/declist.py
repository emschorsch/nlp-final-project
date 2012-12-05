"""
Lab 07 by Emanuel Schorsch
12. When we implemented the decision list and trained it on the test data
    we got an accuracy of 58.72%. This outperformed the MFS by a non-trivial
    6%. This is comforting that our system is better than the second most
    naive system possible.
13. Some of the rules with the highest scores are rules that don't seem to
    be indicative of a specific sense. Some of these include 'organization .'
    This collocation does not seem to say anything meaningful about the type
    of organization it is as presumably many different kinds of 'organization'
    can come at the end of sentences. Another example is the highest scoring
    word. This one is a bag of words feature of the word 'had'. This is a
    very common word which could be within 10 words of nearly any different
    sense of organization. 
    Case-folding would not significantly improve the scores. Upper cases 
    are usually uniformly distributed across different senses so lower
    casing everything will not have an impact. In the cases in which
    upper cases are skewed towards one sense then lower casing everything
    will actually make the decision list worse as the upper cased word
    was actually a decent indicator of the sense in which it is predominantly
    represented in.
    Removing common words might not neccessarily be a good thing. If the bag
    of words is taken from very nearby then the words have more meaning.
    In this case it might be that a high representation of common words such 
    as 'had' or 'the' might indicate either a possesive entity or a specific
    entity. This appears in 'organization.n' where 'had' might have a very 
    high score since organizations as in the entity commonly have items or 
    qualities. Additionally if we were talking about the relief organization
    then 'the' might appear more commonly than it would among a more generic
    version of organization.
    I did not implement stopwords.
14. Intuitively stopping before the end of decision list and simply returning 
    the MFS makes sense. MFS is a fairly powerful simple guess for what sense
    a word is. For words that are triggering rules way down in the decision
    list we are guessing off of rules that have much less predictive power of
    what sense the word is. Presumably then the MFS would be a better guess.
    However, when I implemented stopping when the score fell below 1.0 my
    accuracy went down. This is surprising and may be because the words which
    have none of the features high up on the decision list are usually unusual
    words with never before seen senses. Then guessing the most frequent sense
    would actually be a worst guess then merely guessing randomly. This
    could possibly explain our worse results.
"""


#!/usr/bin/env python
from math import log

"""
Starting point code for the decision list classifier in Lab 07
"""
from parse import getData
from warmup import *


"""
returns a list of all the features in the train data
"""
def getFeatures(data, key, k):
  featureList = []
  for instance in data[key].keys():
    words = data[key][instance]['words']
    tlist = data[key][instance]['heads']
    for i in xrange(0,len(tlist)):
      t = tlist[i]
      featureList.extend(words[max(t-k,0):t])
      featureList.extend(words[t+1:t+k])
  return set(featureList)

"""
returns a dict with num of times each word appeared within k of key
"""
def countf(data, key, k, instanceList):
  countDict = {}
  for instance in instanceList:
    words = data[key][instance]['words']
    tlist = data[key][instance]['heads']
    t = tlist[0]
    if(t == 0):
      post = words[t]+" "+words[t+1]
      countDict[post] = countDict.get(post, 0) + 1
    elif(t == len(words) - 1):
      pre = words[t-1]+" "+words[t]
      countDict[pre] = countDict.get(pre, 0) + 1
    else:
      post = words[t]+" "+words[t+1]
      countDict[post] = countDict.get(post, 0) + 1
      pre = words[t-1]+" "+words[t]
      countDict[pre] = countDict.get(pre, 0) + 1

    words = words[max(t-k,0):t]+words[t+1:t+k]
    wordCount = (map(lambda x: (words.count(x), x), set(words)))
    
    for tup in wordCount:
      countDict[tup[1]] = countDict.get(tup[1], 0) + tup[0]

  return countDict

"""
returns a list of all the instances of a given sense
"""
def instanceSense(data, key, sense):
  return filter(lambda x: sense in data[key][x]['answers'], data[key].keys())

"""
returns a list of all the instances of a word
"""
def getInstances(data, key):
   return data[key].keys()


"""
returns the score
"""
def score(fpos_count, ftot_count):
  alpha = 0.1
  num = fpos_count + alpha
  denom = (ftot_count - fpos_count) + alpha
  return log(num/denom)

"""
returns the top matching sense in the decision list
"""
def getDecision(decList, key, instance, k, testData):
  twords = testData[key][instance]['words']
  tlist = testData[key][instance]['heads']
  t = tlist[0]
  words = []
  if(t == 0):
    post = twords[t]+" "+twords[t+1]
    words.append(post)
  elif(t == len(twords) - 1):
    pre = twords[t-1]+" "+twords[t]
    words.append(pre)
  else:
    post = twords[t]+" "+twords[t+1]
    pre = twords[t-1]+" "+twords[t]
    words.append(post)
    words.append(pre)

  words.extend(twords[max(t-k,0):t]+twords[t+1:t+k])
 
  for rule in decList[key]:
    if rule[1][1] in words:
      return rule[1][0]
    if rule[0] < 0:
      break
  
  tsenses = getSenses(testData, key)
  tsenseFreq = map(lambda x: (x, tsenses.count(x)), set(tsenses))
  mfs = freqSense(tsenseFreq)[0]
  return mfs


if __name__=='__main__':
    trainingFile = '/data/cs65/senseval3/train/EnglishLS.train'
    data = getData(trainingFile)
    testingFile = '/data/cs65/senseval3/test/EnglishLS.test'
    testData = getData(testingFile)
    k = 10
    mfs = {}  #values are tuples of mfs, count of mfs
    decList = {}
    for key in data.keys():
      senses = list(set(getSenses(data, key)))
      #below is list of frequencies
      senseFreq = map(lambda x: (x, senses.count(x)), set(senses))
      mfs[key] = freqSense(senseFreq)[0]
      scores = []
      counts = {}
      for sense in senses:
        senseInst = instanceSense(data, key, sense)
        counts[sense] = countf(data, key, k, senseInst)
        #scores.append( ( score(data, key, word, k, sense), (sense, word) ) )
          #where do we draw the words from?????
      allSenses = {}
      for sense in senses:
        for word in counts[sense].keys():
          allSenses[word] = allSenses.get(word, 0) + counts[sense][word]

      for sense in senses:
        for word in counts[sense].keys():
          w_score = score(counts[sense][word], allSenses[word])
          scores.append( (w_score, (sense, word)) )
      scores.sort(reverse = True)
      #print "len", len(allSenses.keys())
      #print allSenses['to']
      #print counts['369204']
      #print scores[0], key
      #print scores[1], key
      #print scores[2], key
      decList[key] = scores

    count = 0
    correctRando = 0
    correctFreq = 0
    tcount = 0
    tcorrectRando = 0
    tcorrectFreq = 0
    matches = 0
    keys = testData.keys()
    for key in keys:
      tsenses = getSenses(testData, key)
      instances = getInstances(testData, key)
      for inst in instances:
        answer = getDecision(decList, key, inst, k, testData)
        tcorrectFreq += isCorrect(testData, key, inst, answer)
      tcount += len(tsenses)
      tcorrectRando += len(tsenses)/float(len(set(tsenses)))
    print "declist: {0}%".format(tcorrectFreq/float(tcount))



      


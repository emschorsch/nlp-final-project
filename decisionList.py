from math import log
from dataParse import parseA
from collections import defaultdict
import operator
# ----------------------------------------------------------------- #

def getScores(scores,mfp):
  alpha = 0.1
  for word in mfp.keys():
    total = 0.0
    for polar in mfp[word].keys():
      total += mfp[word][polar]
    for polar in mfp[word].keys():
      currentScore = log(mfp[word][polar]/total)
      if currentScore >= scores[word]['score']:
        if mfp[word]['polar'] == 0:
          print word,mfp[word].keys()
        scores[word]['score'] = currentScore
        scores[word]['polar'] = polar

# ----------------------------------------------------------------- #

def decisionList(trainA):
  k = 10
  decList = []
  mfp = defaultdict(lambda: defaultdict(int))
  scores = defaultdict(lambda: defaultdict(int))

  # get the counts of the mfp (most frequent polarity) of each unigram
  for ID in trainA.keys():
    for pos in trainA[ID].keys():
      start, end = pos
      tweet = (trainA[ID][pos]['tweet']).split()[int(start):int(end)]
      for word in tweet:
        polar = trainA[ID][pos]['polar']
        if polar == 'polar': 
          print 'found one'
        mfp[word][polar] += 1

  # get the highest score for each unigram and its associated polarity
  getScores(scores,mfp)
  scoresSort = []
  for word in scores.keys():
    scoresSort.append((word, scores[word]['polar'], scores[word]['score']))
  scoresSort = sorted(scoresSort, key=operator.itemgetter(1), reverse = True)
  
  for item in scoresSort:
    print 'Word: %15s\tPolarity: %s' %(item[0],item[1])
    

# ----------------------------------------------------------------- #      

if __name__ == '__main__':
  trainingFile = 'trainA.txt'
  trainA = parseA(trainingFile)
  decisionList(trainA)

# ----------------------------------------------------------------- #

from math import log
from dataParse import parseA
from collections import defaultdict
from operator import itemgetter
# ----------------------------------------------------------------- #

'''
def getScores(scores,mfp):
  alpha = 0.1
  for word in mfp.keys():
    total = 0.0
    for polar in mfp[word].keys():
      total += mfp[word][polar]
    for polar in mfp[word].keys():
      currentScore = log((mfp[word][polar]+alpha)/(total+alpha))
      if currentScore >= scores[word]['score']:
        scores[word]['score'] = currentScore
        scores[word]['polar'] = polar
'''

def getScores(scores,mfp):
  alpha = 0.1
  for word in mfp.keys():
    wordScores = []
    total = mfp[word]['count'] + alpha
    for polar in mfp[word].keys():
      if polar != 'count':
        count = mfp[word][polar] + alpha
        score = log(count/total)
        wordScores.append((word,polar,score))
    
    topScore = sorted(wordScores, key=itemgetter(2), reverse=True)[0]
    scores[word]['polar'] = topScore[1]
    scores[word]['score'] = topScore[2]  

# ----------------------------------------------------------------- #

def decisionList(trainA):
  k = 10
  decList = []
  mfp = defaultdict(lambda: defaultdict(int))
  scores = defaultdict(lambda: defaultdict(int))

  # get counts of the mfp (most frequent polarity) of each unigram and bigram
  for ID in trainA.keys():
    for pos in trainA[ID].keys():
      start, end = pos
      tweet = (trainA[ID][pos]['tweet']).split()[int(start):int(end)]
      for word in tweet:
	word = word.lower().strip('\'\"!@#$%^&*(),.?<>;:-')
        polar = trainA[ID][pos]['polar']
        mfp[word][polar] += 1.0
        mfp[word]['count'] += 1.0
      for i in range(1,len(tweet)):
        w1 = tweet[i-1].lower().strip('\'\"!@#$%^&*(),.?<>;:')
	w2 = tweet[i].lower().strip('\'\"!@#$%^&*(),.?<>;:')
        bigram = w1 + ' ' + w2
        polar = trainA[ID][pos]['polar']
        mfp[bigram][polar] += 1.0
        mfp[bigram]['count'] += 1.0
  
  # get the highest score for each unigram and its associated polarity
  getScores(scores,mfp)
  scoresSort = []
  for word in scores.keys():
    scoresSort.append((word, scores[word]['polar'], scores[word]['score']))
  scoresSort = sorted(scoresSort, key=itemgetter(2), reverse = False)
  
  for item in scoresSort:
    print 'Word(s): %15s\tPolarity: %s' %(item[0],item[1])
    

# ----------------------------------------------------------------- #      

if __name__ == '__main__':
  trainingFile = 'trainA.txt'
  trainA = parseA(trainingFile)
  decisionList(trainA)

# ----------------------------------------------------------------- #

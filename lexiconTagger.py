from decisionParse import parseB, parseA
from sentimentWords import getSentimentWords
from collections import defaultdict
from checkTags import checkTagsA, checkTagsB

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
        word = word.lower().strip(",!@#$%^&*./\"\'")

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
        tagsA[ID][index] = 'objective'
   
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
        tagsB[ID][subject] = 'objective'
  
  return tagsA, tagsB
# ----------------------------------------------------------------- #

if __name__ == '__main__':
  trainingFileA = 'trainA.txt'
  trainingFileB = 'trainB.txt'
  lexiconFile   = 'sentimentLexicon.txt'
  trainA  = parseA(trainingFileA)
  trainB  = parseB(trainingFileB)
  lexicon = getSentimentWords(lexiconFile)
  tagsA, tagsB = lexiconTag(trainA, trainB, lexicon)
  checkTagsA(tagsA,trainA)
  checkTagsB(tagsB,trainB)

# ----------------------------------------------------------------- #

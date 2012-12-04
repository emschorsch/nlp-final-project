from decisionParse import parseB, parseA
from sentimentWords import getSentimentWords

# ----------------------------------------------------------------- #

def lexiconTag(trainA, trainB, lexicon):
  
  # Use Lexicon to tag data from trainA

  # Use Lexicon to tag data from trainB 
  
# ----------------------------------------------------------------- #

if __name__ == '__main__':
  trainingFileA = 'trainA.txt'
  trainingFileB = 'trainB.txt'
  lexiconFile   = 'sentimentLexicon.txt'
  trainA  = parseA(trainingFileA)
  trainB  = parseB(trainingFileB)
  lexicon = getSentimentWords(lexiconFile)
  tags = lexiconTag(trainA, trainB, lexicon)

# ----------------------------------------------------------------- #

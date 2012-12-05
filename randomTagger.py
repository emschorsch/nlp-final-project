from decisionParse import parseA, parseB
from sentimentWords import getSentimentWords
from collections import defaultdict
from random import *

# ----------------------------------------------------------------- #
def randomTagA(trainA, testA):
  '''
  Takes in two sources of data (test and train for a) and then 
  genterates tags based on the frequency of the tags found in 
  the test data and applies them to the train data
  '''

  # Get counts for trainA
  posAC = negAC = neutAC = objAC = totalAC = 0.0
  for ID in trainA.keys():
    for index in trainA[ID].keys():
      if trainA[ID][index]['polar'] == 'positive':  posAC  += 1
      if trainA[ID][index]['polar'] == 'negative':  negAC  += 1
      if trainA[ID][index]['polar'] == 'neutral':   neutAC += 1
      if trainA[ID][index]['polar'] == 'objective': objAC  += 1
      totalAC += 1
  
  print '[Task A] Pos: %.0f Neg: %.0f Neut: %.0f Obj: %.0f' \
      %(posAC, negAC, neutAC, objAC)

  # Get percents for trainA
  posAP  = posAC/totalAC
  negAP  = negAC/totalAC
  neutAP = neutAC/totalAC
  objAP  = objAC/totalAC
  
  # Use percents to randomly tag words and check correctness of tag
  correctA = 0.0
  for ID in testA.keys():
    for index in testA[ID].keys():
      currentPolar = testA[ID][index]['polar']
      percent = random()
      if percent > (1 - objAP): guess = 'objective'
      elif percent > (1 - posAP - negAP): guess = 'negative'
      elif percent > (1 - posAP - negAP - neutAP): guess = 'neutral'
      else: guess = 'positive'
      if currentPolar == guess:
        correctA += 1

  print '[Task A] Percent Correct:  %f (%.0f/%.0f)' \
      %(correctA/totalAC, correctA, totalAC)
# ----------------------------------------------------------------- #
def randomTagB(trainB, testB):
  '''
  Takes in two sources of data (test and train for B) and then 
  genterates tags based on the frequency of the tags found in 
  the test data and applies them to the train data
  '''

  # Get counts for trainB
  posBC = negBC = neutBC = objBC = totalBC = 0.0
  for ID in trainB.keys():
    for subject in trainB[ID].keys():
      if trainB[ID][subject]['polar'] == 'positive':  posBC  += 1
      if trainB[ID][subject]['polar'] == 'negative':  negBC  += 1
      if trainB[ID][subject]['polar'] == 'neutral':   neutBC += 1
      if trainB[ID][subject]['polar'] == 'objective': objBC  += 1
      totalBC += 1
  
  print '[Task B] Pos: %.0f Neg: %.0f Neut: %.0f Obj: %.0f' \
      %(posBC, negBC, neutBC, objBC)

  # Get percents for trainB
  posBP  = posBC/totalBC
  negBP  = negBC/totalBC
  neutBP = neutBC/totalBC
  objBP  = objBC/totalBC
  
  print negBP, posBP

  # Use percents to randomly tag words and check correctness of tag
  correctB = 0.0
  for ID in testB.keys():
    for subject in testB[ID].keys():
      currentPolar = testB[ID][subject]['polar']
      percent = random()
      if percent > (1 - objBP): guess = 'objective'
      elif percent > (1 - posBP - negBP): guess = 'negative'
      elif percent > (1 - posBP - negBP - neutBP): guess = 'neutral'
      else: guess = 'positive'

      if currentPolar == guess:
        correctB += 1

  print '[Task B] Percent Correct:  %f (%.0f/%.0f)' \
      %(correctB/totalBC, correctB, totalBC)

# ----------------------------------------------------------------- #
if __name__ == '__main__':
  trainingFileA = 'trainA.txt'
  trainingFileB = 'trainB.txt'
  trainA  = parseA(trainingFileA)
  trainB  = parseB(trainingFileB)
  randomTagA(trainA, trainA)
  randomTagB(trainB, trainB)
# ----------------------------------------------------------------- #

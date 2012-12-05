POLAR = 4 #the index of the polarity

# ----------------------------------------------------------------- #

def checkTagsA(tagsA,testA):
  '''
  Takes in a dictionay of the test data and guessed tags for Task A.
  then determines the correctness of the tags, counting true and
  false guesses for each sentiment class.
  '''

  TPos = TNeg = TObj = TNeut = FPos = FNeg = FObj = FNeut = 0.0
  correct = total = 0.0

  for ID in testA.keys():
    for index in testA[ID].keys():

      # Check if guess is corerct
      polar = testA[ID][index]['polar']
      guess = tagsA[ID][index]
      if guess == polar:
        correct += 1

      # Keep track of true and false assignments  
      if   guess == 'positive'  and guess == polar: TPos  += 1
      elif guess == 'negative'  and guess == polar: TNeg  += 1
      elif guess == 'neutral'   and guess == polar: TNeut += 1
      elif guess == 'objective' and guess == polar: TObj  += 1

      elif guess == 'positive'  and guess != polar: FPos  += 1
      elif guess == 'negative'  and guess != polar: FNeg  += 1
      elif guess == 'neutral'   and guess != polar: FNeut += 1
      elif guess == 'objective' and guess != polar: FObj  += 1  

      total += 1

  print '[Task A] Percent Correct: %.2f (%.0f/%.0f)' \
      %(correct/total, correct, total)
  print "True Pos: %d\tFalse Pos: %d" %(TPos,FPos)
  print "True Neg: %d\tFalse Neg: %d" %(TNeg,FNeg)
  print "True Neut: %d\tFalse Neut: %d" %(TNeut,FNeut)
  print "True Obj: %d\tFalse Obj: %d" %(TObj,FObj)

# ----------------------------------------------------------------- #

def checkTagsB(tagsB,testB):

  '''
  Takes in a dictionay of the test data and guessed tags for Task B.
  then determines the correctness of the tags, counting true and
  false guesses for each sentiment class.
  '''

  TPos = TNeg = TObj = TNeut = FPos = FNeg = FObj = FNeut = 0.0
  correct = total = 0.0

  for ID in testB.keys():
    for subject in testB[ID].keys():

      # Check if guess is corerct
      polar = testB[ID][subject]['polar']
      guess = tagsB[ID][subject]
      if guess == polar:
        correct += 1

      # Keep track of true and false assignments  
      if   guess == 'positive'  and guess == polar: TPos  += 1
      elif guess == 'negative'  and guess == polar: TNeg  += 1
      elif guess == 'neutral'   and guess == polar: TNeut += 1
      elif guess == 'objective' and guess == polar: TObj  += 1

      elif guess == 'positive'  and guess != polar: FPos  += 1
      elif guess == 'negative'  and guess != polar: FNeg  += 1
      elif guess == 'neutral'   and guess != polar: FNeut += 1
      elif guess == 'objective' and guess != polar: FObj  += 1  

      total += 1

  print '[Task B] Percent Correct: %.2f (%.0f/%.0f)' \
      %(correct/total, correct, total)
  print "True Pos: %d\tFalse Pos: %d" %(TPos,FPos)
  print "True Neg: %d\tFalse Neg: %d" %(TNeg,FNeg)
  print "True Neut: %d\tFalse Neut: %d" %(TNeut,FNeut)
  print "True Obj: %d\tFalse Obj: %d" %(TObj,FObj)

# ----------------------------------------------------------------- #


def checkListTags(tagsA,testA,task):
  '''
  Takes in test data in list form and a list of guessed tags for Task task.
  then determines the correctness of the tags, counting true and
  false guesses for each sentiment class.
  '''

  TPos = TNeg = TObj = TNeut = FPos = FNeg = FObj = FNeut = 0.0
  correct = total = 0.0

  for i in xrange(0,len(testA)):
      # Check if guess is corerct
      polar = testA[i][POLAR]
      guess = tagsA[i][1]
      if guess == polar:
        correct += 1

      # Keep track of true and false assignments  
      if   guess == 'positive'  and guess == polar: TPos  += 1
      elif guess == 'negative'  and guess == polar: TNeg  += 1
      elif guess == 'neutral'   and guess == polar: TNeut += 1
      elif guess == 'objective' and guess == polar: TObj  += 1

      elif guess == 'positive'  and guess != polar: FPos  += 1
      elif guess == 'negative'  and guess != polar: FNeg  += 1
      elif guess == 'neutral'   and guess != polar: FNeut += 1
      elif guess == 'objective' and guess != polar: FObj  += 1  

      total += 1

  print '%s Percent Correct: %.2f (%.0f/%.0f)' \
      %(task, correct/total, correct, total)
  print "True Pos: %d\tFalse Pos: %d" %(TPos,FPos)
  print "True Neg: %d\tFalse Neg: %d" %(TNeg,FNeg)
  print "True Neut: %d\tFalse Neut: %d" %(TNeut,FNeut)
  print "True Obj: %d\tFalse Obj: %d" %(TObj,FObj)

# ----------------------------------------------------------------- #


#!/usr/bin/python
'''
Parse the Task A and Task B data from the SemEvel Competition

Usage parseB(): 
  data[SID\tUID]['subject'] 	        - gives the subjects associated with
                                          the given ID
  data[SID\tUID][<subject>]['polar'] 	- the tag of the subject
  data[SID\tUID][<subject>]['tweet']    - the contents of the tweet

Usage parseA():
  data[SID\tUID]['index']       	- the parts of the phrase to be indexed
  data[SID\tUID][<index>]['polar'] 	- the tag of the phrase
  data[SID\tUID][<index>]['tweet']	- the contents of the tweet  
'''
#-----------------------------------------------------------------------------#
PERCENTTRAIN = .8
PERCENTTEST  = .2
from collections import defaultdict
#-----------------------------------------------------------------------------#

def getTotalLines(filename):
  count = 0
  for line in open(filename, 'r'):
    count += 1
  return count

#-----------------------------------------------------------------------------#

def parseB(filename):
  totalLines = getTotalLines(filename)
  count = 1

  data = defaultdict(lambda: defaultdict(lambda: defaultdict(str)))
  test = defaultdict(lambda: defaultdict(lambda: defaultdict(str)))

  infile = open(filename, 'r')
  for line in infile:
    line = line.strip().split('\t')    
    if count < int(totalLines*PERCENTTRAIN):
      dictID = line[0]+'\t'+line[1]
      data[dictID][line[2]]['polar'] = line[3].strip('\"')
      data[dictID][line[2]]['tweet'] = line[4]
    if count >= int(totalLines*(1-PERCENTTEST)): 
      dictID = line[0]+'\t'+line[1]
      test[dictID][line[2]]['polar'] = line[3].strip('\"')
      test[dictID][line[2]]['tweet'] = line[4]
    count += 1
  infile.close()
  return data, test

#-----------------------------------------------------------------------------#

def parseA(filename):
  totalLines = getTotalLines(filename)
  count = 1

  data = defaultdict(lambda: defaultdict(lambda: defaultdict(str)))
  test = defaultdict(lambda: defaultdict(lambda: defaultdict(str)))

  infile = open(filename, 'r')
  for line in infile:
    line = line.strip().split('\t')    
    if count < int(totalLines*PERCENTTRAIN):
      dictID = line[0]+'\t'+line[1]
      index = (line[2],line[3])
      data[dictID][index]['polar'] = line[4].strip('\"')
      data[dictID][index]['tweet'] = line[5]
    if count >= int(totalLines*(1-PERCENTTEST)):
      dictID = line[0]+'\t'+line[1]
      index = (line[2],line[3])
      test[dictID][index]['polar'] = line[4].strip('\"')
      test[dictID][index]['tweet'] = line[5]
    count += 1
  infile.close()
  return data, test

#-----------------------------------------------------------------------------#

if __name__ == '__main__':
  trainingFileA = 'trainA.txt'
  trainingFileB = 'trainB.txt'
  trainingDataA, testDataA = parseA(trainingFileA)
  trainingDataB, testDataB = parseB(trainingFileB)
  
  '''
  for ID in testDataB.keys():
    for subject in testDataB[ID].keys():
      polar = testDataB[ID][subject]['polar']
      tweet = testDataB[ID][subject]['tweet']
      print '%s\t%s\t%s\t%s' %(ID,subject,polar,tweet)
  
  for ID in trainingDataB.keys():
    for subject in trainingDataB[ID].keys():
      polar = trainingDataB[ID][subject]['polar']
      tweet = trainingDataB[ID][subject]['tweet']
      print '%s\t%s\t%s\t%s' %(ID,subject,polar,tweet)

  for ID in trainingDataA.keys():
    for index in trainingDataA[ID].keys():
      polar = trainingDataA[ID][index]['polar']
      tweet = trainingDataA[ID][index]['tweet']
      print '%s\t%s\t%s\t%s' %(ID,index,polar,tweet)
  '''

#-----------------------------------------------------------------------------#

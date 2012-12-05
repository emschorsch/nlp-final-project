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
from collections import defaultdict
#-----------------------------------------------------------------------------#
def parseB(filename):
  data = defaultdict(lambda: defaultdict(lambda: defaultdict(str)))
  infile = open(filename, 'r')
  for line in infile:
    line = line.strip().split('\t')
    if len(line) == 5:
      if line[4] != 'Not Available':
        dictID = line[0]+'\t'+line[1]
        data[dictID][line[2]]['polar'] = line[3].strip('\"')
        data[dictID][line[2]]['tweet'] = line[4]
  infile.close()
  return data
#-----------------------------------------------------------------------------#
def parseA(filename):
  data = defaultdict(lambda: defaultdict(lambda: defaultdict(str)))
  infile = open(filename, 'r')
  for line in infile:
    line = line.strip().split('\t')
    if len(line) == 6:
      if line[5] != 'Not Available':
        dictID = line[0]+'\t'+line[1]
        index = (line[2],line[3])
        data[dictID][index]['polar'] = line[4].strip('\"')
        data[dictID][index]['tweet'] = line[5]
  infile.close()
  return data
#-----------------------------------------------------------------------------#
if __name__ == '__main__':
  trainingFileA = 'trainA.txt'
  trainingFileB = 'trainB.txt'
  trainingDataA = parseA(trainingFileA)
  trainingDataB = parseB(trainingFileB)
  
  total = 0

  '''
  for ID in trainingDataB.keys():
    for subject in trainingDataB[ID].keys():
      polar = trainingDataB[ID][subject]['polar']
      tweet = trainingDataB[ID][subject]['tweet']
      print '%s\t%s\t%s\t%s' %(ID,subject,polar,tweet)
      total += len(trainingDataB[ID].keys())
  print total 
  
  '''  

  for ID in trainingDataA.keys():
    for index in trainingDataA[ID].keys():
      polar = trainingDataA[ID][index]['polar']
      tweet = trainingDataA[ID][index]['tweet']
      print '%s\t%s\t%s\t%s' %(ID,index,polar,tweet)
      total += len(trainingDataB[ID].keys())
  print total
#-----------------------------------------------------------------------------#

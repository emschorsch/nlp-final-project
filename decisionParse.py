'''
Parse the Task A and Task B data from the SemEvel Competition

Usage parseB(): 
  data[SID\tUID]['subject'] 	- gives the subject to be tagged
  data[SID\tUID]['tag'] 	- the tag of the subject
  data[SID\tUID]['tweet']	- the contents of the tweet

Usage parseA():
  data[SID\tUID]['start'] 	- the start of the phrase
  data[SID\tUID]['end']		- the end of the phrase
  data[SID\tUID]['tag'] 	- the tag of the phrase
  data[SID\tUID]['tweet']	- the contents of the tweet  
'''

from collections import defaultdict

def parseB(filename):
  data = defaultdict(lambda: defaultdict(str))
  infile = open(filename,'r')
  for line in infile:
    line = line.strip().split('\t')
    if len(line) == 5:
      dictID = line[0]+'\t'+line[1]
      data[dictID]['subject'] = line[2]
      data[dictID]['tag'] = line[3]
      data[dictID]['tweet'] = line[4]
  return data 

def parseA(filename):
  data = defaultdict(lambda: defaultdict(str))
  infile = open(filename,'r')
  for line in infile:
    line = line.strip().split('\t')
    if len(line) == 6:
      dictID = line[0]+'\t'+line[1]
      data[dictID]['start'] = line[2]
      data[dictID]['end'] = line[3]
      data[dictID]['tag'] = line[4]
      data[dictID]['tweet'] = line[5]
  return data

if __name__ == '__main__':
  trainingFileA = 'outputTestA.txt'
  trainingFileB = 'outputTestB.txt'
  trainingFileA = parseA(trainingFileA)
  trainingDataB = parseB(trainingFileB)


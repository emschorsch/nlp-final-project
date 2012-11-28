#! /usr/bin/python
"""
Implements a sentiment analyzer. The analyzer trains on annotated tweets.
A few different methods are implemented to identify the sentiment of a new 
tweet.
1) A simple count of the number of sentiment types
2) something complicated
"""


#some global values
TRAINFILE = 'outputTestA.txt'
POLAR = 4 #the index of the polarity
TWEET = 5 #the index of the tweet itself

"""
builds a list of the data based on the info in filename
"""
def extractData( fileName ):
  #build the list of test words
  f = open(TRAINFILE, 'r')
  trainData = map(lambda f: f.strip('\n').split('\t'), f.readlines())
  f.close()
  return trainData





def main():
  trainData = extractData( TRAINFILE )
  print trainData[0][POLAR]


if __name__=='__main__':
  main()


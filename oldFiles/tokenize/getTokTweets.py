#!/usr/bin/python
def getTokTweets(filename):
  infile = open(filename,'r')
  for line in infile:
    line = line.strip().split('\t')
    tweet = line[0]
    print tweet

if __name__ == '__main__':
  trainingFile = 'trainB.txt'
  tweets = 'tokenizedTweets.txt'
  getTokTweets(tweets)

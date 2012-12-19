#!/usr/bin/python
def getTokTweetsList(filename):
  infile = open(filename,'r')
  return [tweet.strip() for tweet in infile]

def addTokTweets(tokTweets,filename):
  infile = open(filename,'r')
  index = 0
  for line in infile:
    line = line.strip().split('\t')
    line[4] = tokTweets[index]
    print '%s\t%s\t%s\t%s\t%s' %(line[0], line[1], line[2], line[3], line[4])
    index += 1

if __name__ == '__main__':
  trainingFile = 'trainB.txt'
  tokTweetsFile = 'tokTweetsOnly.txt'
  tokTweets = getTokTweetsList(tokTweetsFile)
  addTokTweets(tokTweets, trainingFile)

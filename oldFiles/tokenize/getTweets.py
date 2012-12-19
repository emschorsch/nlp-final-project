#!/usr/bin/python
def getTweets(filename):
  infile = open(filename,'r')
  for line in infile:
    line = line.strip().split('\t')
    tweet = line[4]
    print tweet

if __name__ == '__main__':
  filename = 'trainB.txt'
  getTweets(filename)

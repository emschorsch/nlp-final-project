#!/usr/bin/env python
"""
Lab 07 by Emanuel Schorsch
1. There were 57 different lexelts. 
2. There are 5 adjectives, 20 nouns, and 32 verbs
3. There are 112 training examples for the noun "organization"
        "U" is not counted as a sense for the rest of the problems unless 
        specified afterward.
4. There are 4 senses of "organization.n"
5. If we guessed randomly we would get 20.97% correct.
6. The most frequent sense for "organization.n" is 
  'organization%1:14:00::' with 88 occurences.
7. Using the most frequent sense baseline where it is marked correct if
   it explicitly matches one of the given senses for the word (including "U")
   we get 53.83%.
8. There are 56 examples of "organization.n" in the test data.
9a. There is one sense that appears in the train data and not the test data.
    It is 'organization%1:04:00::'. This is not a problem other than wasted
    computation since we are getting more diverse knowledge than we end up
    being tested on. This is the way every test works in the real world.
9b. There are two sense that appear in the test data and not the train data.
    The two new senses for 'organization.n' are 'organization%1:07:00::'
    and 'organization%1:04:01::'. This is a serious problem since we have no 
    exposure to this sense and thus have little to no information on it. This
    makes it almost impossible to correctly classify words in the test data
    into this new unseen sense.
10. There are 44 words that have the same most frequent sense in the 
    training data and test data. This is 77.19% of the word types. This
    means the percentage we got in 7 should be lower when calculated
    for the test data since it is not truly the most frequent sense in 
    25% of the words.
11. The MFS accuracy when computed on the test data is 52.4%. This is higher
    than the random baseline which for the test data is 22.4%. I expected the
    MFS to perform better than the random baseline. However, it is surprising
    that the percentage wasn't lower than when it was applied to the training
    data. One explanation for this is that even the words whose most frequent
    sense differs the difference is not by a huge amount so the percentage
    is not as drastically lower as would be expected.
"""




"""
Starting point code for the warmups in Lab 07
"""
from parse import getData

"""
returns the number of words correctly labeled
"""
def corrStats(testData, word, sense):
    keys = testData[word].keys()
    count = 0
    for key in keys:
      count+= isCorrect(testData, word, key, sense)
    return count
    #int(filter(lambda x: mfs[0] == x[0], tsenseFreq)[0][1])

"""
returns whether a given word is correctly labeled
"""
def isCorrect(testData, word, instance, sense):
    return sense in testData[word][instance]['answers']

"""
returns a list of all the senses for the given word
"""
def getSenses(trainData, word):
    answers = []
    keys = trainData[word].keys()
    for key in keys:
        answers.extend(trainData[word][key]['answers'])
    return filter(lambda x: x!= "U", answers)

"""
returns a sorted list, in descending order, of all the senses tupled with
their counts
"""
def freqSense(senses):
    return sorted(senses, key=lambda x: x[1], reverse=True)

"""
def freqCountList(senses, key):
    filter(lambda x: key == senses[0], senses)
"""

      

if __name__=='__main__':
    trainingFile = '/data/cs65/senseval3/train/EnglishLS.train'
    trainData = getData(trainingFile)
    testingFile = '/data/cs65/senseval3/test/EnglishLS.test'
    testData = getData(testingFile)
    keys = trainData.keys()
    print "1 {0}".format(len(keys))
    tok = [ word[-1] for word in keys]
    print "2 %s" % zip(set(tok), map(lambda x: tok.count(x), set(tok)))
    print "3 %s" % len(trainData["organization.n"])
    print "4 %s" % len(set(getSenses(trainData, "organization.n")))
    count = 0
    correctRando = 0
    correctFreq = 0
    tcount = 0
    tcorrectRando = 0
    tcorrectFreq = 0
    matches = 0
    for key in keys:
      senses = getSenses(trainData, key)
      tsenses = getSenses(testData, key)
      #below is list of frequencies
      senseFreq = map(lambda x: (x, senses.count(x)), set(senses))
      tsenseFreq = map(lambda x: (x, tsenses.count(x)), set(tsenses))
      mfs = freqSense(senseFreq)[0]
      matches += mfs[0] == freqSense(tsenseFreq)[0][0]
      correctFreq += int(mfs[1])
      tcorrectFreq += corrStats(testData, key, mfs[0])
      count += len(senses)
      tcount += len(tsenses)
      correctRando += len(senses)/float(len(set(senses)))
      tcorrectRando += len(tsenses)/float(len(set(tsenses)))
    print "5 {0}".format(correctRando/float(count))
    otemp = getSenses(trainData, "organization.n")
    org = map(lambda x: (x, otemp.count(x)), set(otemp))
    otemp = getSenses(testData, "organization.n")
    orgTest = map(lambda x: (x, otemp.count(x)), set(otemp))
    #below rich's code easier to do mine
    #print "6 %s" % zip(set(org), map(lambda x: org.count(x), set(org)))
    print "6 {0}".format(map(lambda x: (x, org.count(x)), set(org))[1])
    print "7 {0}".format(correctFreq/float(count))
    print "8 {0}".format(len(testData["organization.n"]))
    uniqTest = filter(lambda x: x[0] not in [y[0] for y in org], orgTest)
    uniqTrain = filter(lambda x: x[0] not in [y[0] for y in orgTest], org)
    print "9a {0}".format(uniqTrain)
    print "9a {0}".format(uniqTest)
    print "10 matches: {0} ie: {1}%".format(matches,matches/float(len(keys)))
    print "trandoCorrect {0}".format(tcorrectRando)
    print "11 rando: {0}%".format(tcorrectRando/float(tcount))
    print "mfs: {0}%".format(tcorrectFreq/float(tcount))

    



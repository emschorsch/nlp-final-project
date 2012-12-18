nlp-final-project: by Justin Cosentino and Emanuel Schorsch
=================

Files pertaining to our NLP Final Project: Semantic Analysis in Twitter

multipleTaggey.py: Contains the sentiment lexicon tagger and the mfs tagger.
        Change globals in dataParse.py in order to change the test data for
        each.

sentimentTagger.py: Contains the naive bayes classifier

decisionList.py: Contains the decision list classifier. Change globals in
        dataParse.py in order to change the size of the test and training data.

checkTags.py: Contains functions used to check the tags of a classifier with
        the correct tags.

dataParse.py: Parsing mechanism used to place data into dictionaries. Used in
        the deicion list and multipleTagger.py.

sentimentLexicon.txt: The text file containing the sentiment lexicon data.

trainA.txt: The training\test data for task A

trainB.txt: The training\test data for task B

results.txt: Results for each classifier

oldFiles\: Old files not being used in the classifiers

texFiles\: LaTeX files used to create our paper

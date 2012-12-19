To tokenize a file of tweets:

run getTweets.py > tweetsOnly.txt
run /scratch/jcosent1/ark/twokenize.sh tweetsOnly.txt > tokenizedTweets.txt
run getTokTweets.py > tokTweeksOnly.txt
run addTokTweets.py > tokenizedTrainB.txt

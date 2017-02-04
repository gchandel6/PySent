import re

# Process tweets and convert into plain form

def processTweet(tweet):

	tweet=tweet.lower()
	tweet=re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
	tweet=re.sub('@[^\s]+','AT_USER',tweet)
	tweet=re.sub('[\s]+', ' ', tweet)
	tweet=re.sub(r'#([^\s]+)', r'\1', tweet)
	tweet=tweet.strip('\'"')

	return tweet



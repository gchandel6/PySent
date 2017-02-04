import nltk
import random

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB ,BernoulliNB

from sklearn.linear_model import LogisticRegression , SGDClassifier
from sklearn.svm import SVC , LinearSVC , NuSVC



#	Building our own Classifier based on votes from other classifiers

from nltk.classify import ClassifierI
from collections import Counter

def my_mode(l):
	c = Counter(l)
	return c.most_common(1)[0][0]


class VoteClassifier(ClassifierI):

	def __init__(self,*classifiers):
		self._classifiers = classifiers

	def classify(self,features):
		votes=[]
		
		for c in self._classifiers:
			v=c.classify(features)
			votes.append(v)

		return my_mode(votes)
	
	def confidence(self,features):
		votes=[]
		
		for c in self._classifiers:
			v=c.classify(features)
			votes.append(v)

		choice_votes = votes.count(my_mode(votes))
		conf = float(choice_votes) / len(votes)
		return conf



#	Taking Input Reviews Data from file

short_pos = open("movie_reviews/short_pos.txt","r").read().decode("utf-8")
short_neg = open("movie_reviews/short_neg.txt","r").read().decode("utf-8")

docs = []

for r in short_pos.split('\n'):
	docs.append( (r , "pos") )

for r in short_neg.split('\n'):
	docs.append( (r , "neg") )

docs=docs[:2000]

all_words = []

short_pos_words = word_tokenize(short_pos)
short_neg_words = word_tokenize(short_neg)


all_stop_words = stopwords.words()

# Building the Feature Vector

for w in short_pos_words:
	if w not in all_stop_words:
		all_words.append(w)

for w in short_neg_words:
	if w not in all_stop_words:
		all_words.append(w)


all_words = nltk.FreqDist(all_words)


word_features = list(all_words.keys())[:1000]


# Method to generate feature vector for a review

def find_features(docs):
	words = set(docs)

	features = {}

	for w in word_features:
		features[w] = (w in words)

	return features


featuresets = [ (find_features(rev),cat) for (rev,cat) in docs]

training_set = featuresets[:1600]
testing_set = featuresets[1600:]


#	Testing Various Classifiers on testing_set

classifier = nltk.NaiveBayesClassifier.train(training_set)

# print("Naive Bayes Classifier Accuracy:",nltk.classify.accuracy(classifier,testing_set)*100)

MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)

BNB_classifier = SklearnClassifier(BernoulliNB())
BNB_classifier.train(training_set)

LR_classifier = SklearnClassifier(LogisticRegression())
LR_classifier.train(training_set)

SGDC_classifier = SklearnClassifier(SGDClassifier())
SGDC_classifier.train(training_set)

LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(training_set)

NuSVC_classifier = SklearnClassifier(NuSVC())
NuSVC_classifier.train(training_set)

#	Our Custom Classifier

voted_classifier = VoteClassifier(classifier,
									MNB_classifier,
									BNB_classifier,
									NuSVC_classifier,
									LinearSVC_classifier,
									SGDC_classifier,
									LR_classifier)

# print("Voted classifier accuracy percent:",(nltk.classify.accuracy(voted_classifier,testing_set))*100 )


pos_words = open("movie_reviews/pos.txt","r").read().decode("utf-8").split(" ")
neg_words = open("movie_reviews/neg.txt","r").read().decode("utf-8").split(" ")


def find_sentiment(text):

	results=[]

	features = find_features(text)
	sent1 = voted_classifier.classify(features)

	results.append(sent1)

	text=text.split(" ")

	pos_cnt=0
	neg_cnt=0

	for t in text:
		if t=="":
			text.remove(t)

	for w in pos_words:
		if w in text:
			pos_cnt=pos_cnt+1

	for w in neg_words:
		if w in text:
			neg_cnt=neg_cnt+1

	if pos_cnt>neg_cnt:
		sent2='pos'
	elif neg_cnt>pos_cnt:
		sent2='neg'
	else:
		sent2='neutral'

	results.append(sent2)

	return sent2

print("Enter Text:")

print(find_sentiment(raw_input()))






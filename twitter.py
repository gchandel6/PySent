from tweepy import Stream 
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json

# import classifier as cl
import processtweet as pw

ckey 	="DCVYc3vaXBFFxuzhjkAsqaXMZ"
csecret ="MkeKSzcdEdfIdniJExtM1vGNIdwg4vWRozvBnOLFUHKeJLxESP"
atoken 	="2501893858-rbaSmdRlOQzmCDQTY4VofWkAn3zlxNEamdvk1hZ"
asecret ="BvBenvyRVtcealpWYl9X0EYWvx2yTMuA1LEjPZ5J4Kor3"

class listener(StreamListener):

	def on_data(self,data):
		
		try:

			all_data = json.loads(data)
			tweet = all_data["text"]

			tweet=pw.processTweet(tweet)

			sentiment = cl.find_sentiment(tweet)
			print(tweet , sentiment )

			if sentiment!= 'neutral':
				output = open("twitter-out.txt","a")
				output.write(sentiment)
				output.write("\n")
				output.close()

			return True

		except:
			return True

	def on_error(self,status):

		print(status) 

auth = OAuthHandler(ckey,csecret)
auth.set_access_token(atoken,asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=['trump'])

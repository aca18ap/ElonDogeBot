from tweepy import StreamListener, OAuthHandler, API, Stream
from usr import getTwitterKeys
from usr import getUsersFromFile
from tweetFinding import coinParse, elonParse
from bc import worthInvesting
from multiprocessing import Queue
import sys

keys = getTwitterKeys()

consumer_secret = keys.get('consumer_secret')
consumer_key = keys.get('consumer_key')
access_token_secret = keys.get('access_token_secret')
access_token = keys.get('access_token')


usersToTrack = getUsersFromFile()
usernames = list(usersToTrack.keys())
userIds =   list(usersToTrack.values())
userIdsInt = [int(x) for x in userIds]


streamOnline = False

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = API(auth)

class TweetStreamListener(StreamListener):
    def on_connect(self):
        print('Registered to twitter stream')

    def on_status(self, status):
        if status.user.id in userIdsInt:
            print("adding tweetID" ,status.id, "to queue")
            jobsQueue.put(status)

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_error disconnects the stream
            return False


def startListening(q):
    global jobsQueue
    jobsQueue = q  
    print("Queue initialized")  
    streamListener = TweetStreamListener()
    stream = Stream(auth = api.auth, listener=streamListener)
    print("Stream started:", stream.running)
    stream.filter(follow=userIds)
    print("filtering following users:", userIds)

def processTweet(status):
    tweetBody = status.text
    ##If tweet creator is in the user's list
    if status.user.id in userIdsInt:
        coinFound = elonParse(tweetBody)
        print(tweetBody)
        if coinFound == None:
            coinFound = coinParse(tweetBody)
        if coinFound != None:
            print("Coin found!! Trading " + coinFound)
            print(usernames[userIds.index(status.user.id_str)], " made the call")
            print(status.user.screen_name, " these should match")
            worthInvesting(usernames[userIds.index(status.user.id_str)], coinFound)
        else:
            print("No coin found or coin not availble in Binance Futures")





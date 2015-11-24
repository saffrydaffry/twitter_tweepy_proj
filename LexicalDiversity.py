__author__ = 'Safyre'
'''
For problem 2.2, download tweets of users in db_restT and compute the lexical diversity of all.  I think
here I will limit to 100 tweets per user, since there are so many in db_restT
'''



import pymongo, tweepy
from nltk.corpus import stopwords
from time import sleep
import json, os
from tempfile import TemporaryFile
from boto.s3.key import Key
from filechunkio import FileChunkIO
from boto.s3.connection import S3Connection
from TweetToMongo import TweetToMongo


print "Access twitter api \n"
consumer_key = "";
consumer_secret = "";

access_token = "";
access_token_secret = "";

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth_handler=auth)


print " Open MongoDB connection to db_restT\n"
try:
    conn=pymongo.MongoClient()
    print "Connected!"
except pymongo.errors.ConnectionFailure, e:
    print "Connection failed : %s" % e


rest_db = conn['db_restT']
rest_coll = rest_db.posts

all_users = rest_coll.find()

print "Extracting list of users\n"
users_list = []
for record in all_users:
    users_list.append(record['user']['screen_name'])
print "Showing first 100 screen names\n"
for user in  users_list[0:100]:
    print user

print "Create new collection to store 500 tweets into called db_lexus"

lex_db = conn['db_lexus2'] #70 users, but only 19 unique
posts = lex_db.posts

lex_dict = {}
unique_users = set(users_list)
print "There are %d users listed, but only %d unique" %(len(users_list), len(set(users_list)))
try:
    for user in unique_users:
        temp_tweet = ""
        print "User: ", user
        for tweet in tweepy.Cursor(api.user_timeline,screen_name=user, wait_on_rate_limit = True).items(1000):
            temp_tweet += tweet._json['text']
            print tweet._json['text']
            #print tweet.text
            #print json.dumps(tweet._json).encode('utf8'),"\n"

        tweet_blob = temp_tweet.split()
        tweet_blob = [word.lower() for word in tweet_blob if word.isalpha() &  len(word)>=3 & (word.lower() not in stopwords.words('english'))]
        tweet_blob2 = tweet_blob
        num_words = len(tweet_blob)

        unique_words = len(set(tweet_blob))
        print "total word count: ", num_words, "unique word count: ", unique_words,"LD: ", float(unique_words)/num_words
        lex_dict['user'] =user
        lex_dict['LD']= float(unique_words)/num_words
        lex_dict['text']=tweet_blob # list of each word after preprocessing
        posts.insert(lex_dict.copy()) #use copy to avoid dup keys error?

except tweepy.TweepError as e:
    print('Below is the printed exception')
    print(e)
    if '401' in e:
        # not sure if this will even work
        print('Disconnection error raised. Attempting to restart: ')
        print(e)
        sleep(60)
        pass
    else:
        raise e
#toMongo = TweetToMongo()
#for user in  users_list[0:10]:
#    toMongo.start()
#    for tweet in tweepy.Cursor(api.user_timeline,screen_name=user, wait_on_rate_limit = True).items(100):
#        toMongo.write2(tweet)
        # FYI: JSON is in tweet._json
#        print tweet._json
#        print tweet.text
#        print json.dumps(tweet._json).encode('utf8'),"\n"
#    toMongo.end2(user)
#    toMongo.push2(lex_db)



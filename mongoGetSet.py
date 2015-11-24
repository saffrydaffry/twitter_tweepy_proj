__author__ = 'Safyre'
'''
First bit: Getting twitter data automatically to mongoDB
'''

import pymongo, tweepy

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



print " Open MongoDB connection\n"
try:
    conn=pymongo.MongoClient()
    print "Connected!"
except pymongo.errors.ConnectionFailure, e:
    print "Connection failed : %s" % e

rest_db = conn['db_restT']
#mem_db = rest_db.my_collection

toMongo = TweetToMongo()
for query in ["#Warriors", "#NBAFinals2015"]:
    toMongo.start()
    for tweet in tweepy.Cursor(api.search,q=query, since = "2015-07-05", until = "2015-07-12", wait_on_rate_limit = True).items(10):
        toMongo.write(tweet)
        # FYI: JSON is in tweet._json
        print tweet._json
        print tweet.text
        print json.dumps(tweet._json).encode('utf8'),"\n"
    toMongo.end()
    toMongo.push(rest_db)

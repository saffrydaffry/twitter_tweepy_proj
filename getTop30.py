__author__ = 'Safyre'

'''
2.1 and 2.3 (partly) Query db_tweets and get list of followers for users with top 30 retweets
'''

import pymongo, itertools, tweepy, time
from FollowersToMongo import FollowersToMongo

print " Open MongoDB connection\n"

try:
    conn = pymongo.MongoClient()
    print "Connected!"
except pymongo.errors.ConnectionFailure, e:
    print "Connection failed : %s" % e

tweets_db = conn['db_tweets']
tweets_coll = tweets_db.posts  # posts is the collection name from previous step

print "the number of records in this collection is : %d \n" % tweets_coll.count()
# x= list(tweets_coll.find_one({'retweet_count' : {'$gt':1263} }))
## take 1000 of the most followed users, guaranteed (almost) to have 30 distinct users
y = tweets_coll.find().sort('user.retweeted_count', -1).limit(1000)  # -1 sorts in descending order
#y = tweets_coll.distinct('user.screen_name').sort('user.followers_count',-1).limit(30)

#for item in x:
#print item
#print tweets_db.collection_names()
print "grab the list of screen_names... \n"
sorted_SN = []
sorted_Loc = []
for record in y:
    #print record['user']['followers_count']
    #print record['user']['screen_name']
    sorted_SN.append(record['user']['screen_name'])
    sorted_Loc.append(record['user']['location'])
#for i in sorted_SN: print i

#[(g[0], len(list(g[1]))) for g in itertools.groupby(['a', 'a', 'b', 'b', 'b'])]
#[('a', 2), ('b', 3)]
condensed_SN = [g[0] for g in itertools.groupby(sorted_SN)]
condensed_Loc = [g[0] for g in itertools.groupby(sorted_Loc)]

print "The top 30 user names by retweet counts are..."
#for i, j in condensed_SN[0:30]: print i,j
top30 = zip(condensed_SN[0:30], condensed_Loc[0:30])
for i, j in top30: print "User name: ", i, ", Location: ", j

print "Getting followers for each user\n"

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
    conn = pymongo.MongoClient()
    print "Connected!"
except pymongo.errors.ConnectionFailure, e:
    print "Connection failed : %s" % e

#follow_db = conn['db_followers']
follow_db = conn['db_followers2'] # second time point

toMongo = FollowersToMongo()

toMongo.start()
for SN in condensed_SN[0:30]:
    print "Sending user names to api.followers\n"
    #for user in tweepy.Cursor(api.followers, wait_on_rate_limit=True, screen_name=SN).items():
    for follower_id in tweepy.Cursor(api.followers_ids, wait_on_rate_limit= True, screen_name = SN).items(40000):
        print "writing followers for user %s" % SN
        #print user._json
        print SN, follower_id
        toMongo.write2(follower_id)
        #toMongo.write(user)
        #time.sleep(60)  # another way to avoid rate limit, but falls behind and gets disconnected...
            # FYI: JSON is in tweet._json
            #print user._json
            #print json.dumps(user._json).encode('utf8'),"\n"
    toMongo.end2(SN)
    toMongo.push2(follow_db)

print "Finished!"



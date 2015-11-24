__author__ = 'Safyre'
'''
2.3 find the number of unfollows after a period of time for the top 10 users in db_tweets
'''

print " Open MongoDB connection \n"
try:
    conn=pymongo.MongoClient()
    print "Connected!"
except pymongo.errors.ConnectionFailure, e:
    print "Connection failed : %s" % e

tweets_db = conn['db_tweets']
tweets_coll = tweets_db.posts

print "Extracting list of users top 10 users by followers count\n"
tweets_records = tweets_coll.find().sort('description.followers_count', -1).limit(10)

print "Show users..."
users_list = []
for record in tweets_records:
    users_list.append(record['user']['screen_name'])
    print record['user']['screen_name']

#users_list = set(users_list)
#print len(set(users_list)) # got 10
#print users_list[69]
print "Grabbing data from db_followers\n"
followers_db = conn['db_followers']
first_coll = followers_db.posts
#first = first_coll.find({'user': {'$in': users_list}})

print "Grabbing data from db_followers2\n"
followers2_db = conn['db_followers2']
second_coll = followers2_db.posts
#second = second_coll.find({'user': {'$in': users_list}})

print "Iterating over follower ids"
for user in users_list:
    first = first_coll.find({'user': user})
    second = second_coll.find({'user': user})
    for record1 in first:
        for record2 in second:
            unfollowed = []
            for id in record1['followers_ids']:#print record2['followers_ids']
                if id not in record2['followers_ids']:
                    unfollowed.append(str(id))
                    #print id
            print "Over 12 hours, ", user, "lost ", len(unfollowed), "followers"
__author__ = 'Safyre'

'''
Part 1.1 Grab files from S3 and store in collection titled db_tweets

'''

import os, pymongo, json
from boto.s3.key import Key
from boto.s3.connection import S3Connection

print "connecting to S3 via boto \n"
conn = S3Connection('', '')
bucket = conn.create_bucket('w205_hw3bucket')  # sub-datasets bucket already exists
myBucket = conn.get_bucket('w205_hw3bucket')

for key in myBucket.list():
    print key.name.encode('utf-8')

wkdir = '/Users/Safyre/Documents/W205-assignments-master/HW3/'
#bucket = conn.create_bucket('w205_hw2bucket')  # sub-datasets bucket already exists
myBucket = conn.get_bucket('w205_hw3bucket')
myKey = Key(myBucket)
bucket_list = myBucket.list()
# awesomeness http://www.laurentluce.com/posts/upload-and-download-files-tofrom-amazon-s3-using-pythondjango/


print " Open MongoDB connection\n"
try:
    conn=pymongo.MongoClient()
    print "Connected!"
except pymongo.errors.ConnectionFailure, e:
    print "Connection failed : %s" % e

tweets_db = conn['db_tweets']


print "downloading new files locally\n"
print "like this: s3_oldfilename.json"
for l in bucket_list:
    print l
    if str(l.key).endswith(".json"):
        keyString = str(l.key)
        # check if file exists locally, if not: download it
        if not os.path.exists(wkdir + "s3_" + keyString):
            print 'Writing to Mongo...'
            fname = wkdir + "s3_" + keyString
            l.get_contents_to_filename(fname)
            posts = tweets_db.posts
            posts.insert(json.load(open(fname,'r')))
            os.remove(fname)

print "Finished!"
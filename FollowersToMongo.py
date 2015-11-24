__author__ = 'Safyre'

import json, os


class FollowersToMongo:
    '''
    Modified tweet serializer
    '''
    out = None
    first = True
    count = 0
    fname = ""
    followers_dict = {}
    followers_list = []

    def start(self):
        self.fname = "temp_followers-"+str(self.count)+".json"
        self.out = open(self.fname,"w+")
        self.out.write("[\n") #add bracket to open list
        self.first = True

    def end(self):
        if self.out is not None:
            self.out.write("\n]\n")
            self.out.close()
        self.out = None

    def write(self, tweet):
        if not self.first:
            self.out.write(",\n")
        self.first = False
        # json uses dictionary, "text" is key for content in tweet
        #self.out.write(json.dumps(tweet._json["text"]))
        self.out.write(json.dumps(tweet._json).encode('utf8'))
        self.count += 1  # count to save a new file

    def push(self, db):
        self.out = open(self.fname,"r")
        posts = db.posts # posts is the name of the collection
        posts.insert(json.load(self.out))
        #os.remove(self.fname)

    def write2(self, followerID):  # modified for skipping writing to file
        self.followers_list.append(followerID)

    def end2(self, user): # modified for skipping writing to file
        self.followers_dict['user'] = user
        self.followers_dict['followers_ids']=self.followers_list

    def push2(self, db):  # modified for skipping reading from file
        posts = db.posts
        posts.insert(self.followers_dict.copy())
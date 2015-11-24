__author__ = 'Safyre'

from tempfile import TemporaryFile
import json, os
import nltk
from nltk.corpus import stopwords

class TweetToMongo:
    '''
    Modified tweet serializer
    '''
    out = None
    first = True
    count = 0
    fname = ""
    temp_tweets = ""
    tweet_blob = []
    lexical_dict = {}

    def start(self):
        self.fname = "temp_tweets-"+str(self.count)+".json"
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
        posts = db.posts
        posts.insert(json.load(self.out))
        os.remove(self.fname)

    def write2(self, tweet):  # modified for skipping writing to file
        tweet_string = json.dumps(tweet._json['text']).encode('utf8')
        self.temp_tweets += tweet_string

    def end2(self, user): # modified for skipping writing to file
        self.lexical_dict['user'] = user
        self.lexical_dict['lexical_diversity']= self._Lexical_Diversity()

    def push2(self, db):  # modified for skipping reading from file
        posts = db.posts.ensure_index(('notification'), unique = True, sparse = True)
        posts.insert(self.lexical_dict)

    #--private method for preprocessing tweets
    def _preprocess(self):
        self.tweet_blob.extend(self.temp_tweets.split())
        self.tweet_blob = [word.lower() for word in self.tweet_blob if word.isalpha() & (word.lower() not in stopwords.words('english'))]
        return(self.tweet_blob)

    def _Lexical_Diversity(self):
        self.tweet_blob = self._preprocess()
        num_words = len(self.tweet_blob)
        #unique_words = len(sorted(set(self.tweet_blob), key=self.tweet_blob.index))
        unique_words = len(set(self.tweet_blob))
        return(num_words/unique_words)





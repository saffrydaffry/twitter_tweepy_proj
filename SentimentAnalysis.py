__author__ = 'Safyre'
# General libraries.
import re
import numpy as np
import matplotlib.pyplot as plt

# SK-learn libraries for learning.
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.grid_search import GridSearchCV

# SK-learn libraries for evaluation.
from sklearn import metrics
from sklearn.metrics import classification_report

# SK-learn library for importing the newsgroup data.
from sklearn.datasets import fetch_20newsgroups

# SK-learn libraries for feature extraction from text.
from sklearn.feature_extraction.text import *


## import training data
train_labels =[]
with open('sentiment_train_dat.txt', 'r') as f:
    train_labels.extend([line.split()[0] for line in f])

with open('sentiment_train_dat.txt', 'r') as f:
    train_dat = [line.split()[1:] for line in f]
## shuffle
train_labels = np.array(train_labels)
train_dat = np.array(train_dat)

## turn each row from list to string
for i in range(0,train_dat.shape[0]):
    train_dat[i] = " ".join(train_dat[i])
print train_labels.shape, train_dat.shape
shuffle = np.random.permutation(np.arange(train_labels.shape[0]))
print train_labels.shape, shuffle.shape
print "Shuffled data"

train_labels = train_labels[shuffle]
train_dat = train_dat[shuffle]

## split to smaller training data and dev data
print "Set up Training Data \n"
mini_train_dat = train_dat[0:6000]
mini_train_labels = train_labels[0:6000]
dev_dat = train_dat[6000:]
dev_labels = train_labels[6000:]

print "Reformatting 6000 sample training data, Just over 1000 allocated for development"
print mini_train_dat.shape
print mini_train_dat[0:10]


## split data with count vectorizer
print "Set up CountVectorizer object\n"
cv = CountVectorizer()
cv_transform = cv.fit_transform(mini_train_dat)
out_dev  = cv.transform(dev_dat)

## set up Log regression
print "Train the classifer and evaluate its accuracy"
Cs = {'C':  [0.01, 0.1, 0.25, 0.5, 0.75, 0.9, 1, 2, 5, 10, 100, 1000]} #can't be zero
logR = LogisticRegression(penalty = 'l2') # L2 Gaussian regularization
logR = GridSearchCV(logR, Cs)
logR.fit(cv_transform, mini_train_labels)

y_pred = logR.predict(out_dev)
print "Accuracy of Logistic Regression data is: %.2f" % logR.score(out_dev, dev_labels)
#print "Other accuracy metric, f1-score %.2f" % metrics.f1_score(dev_labels, y_pred, average= "macro")
print "Optimized C is %d \n" % (logR.best_params_['C'])

Copt = logR.best_params_['C']

## grab raw data from 2.1
import pymongo, itertools, tweepy, time
from FollowersToMongo import FollowersToMongo

print " Open MongoDB connection\n"

try:
    conn = pymongo.MongoClient()
    print "Connected!"
except pymongo.errors.ConnectionFailure, e:
    print "Connection failed : %s" % e

tweets_db = conn['db_tweets']
tweets_coll = tweets_db.posts

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
sorted_tweets = []
for record in y:
    #print record['user']['followers_count']
    #print record['user']['screen_name']
    sorted_SN.append(record['user']['screen_name'])
    sorted_tweets.append(record['text'])
#for i in sorted_SN: print i

#[(g[0], len(list(g[1]))) for g in itertools.groupby(['a', 'a', 'b', 'b', 'b'])]
#[('a', 2), ('b', 3)]
#condensed_SN = [g[0] for g in itertools.groupby(sorted_SN)]

#print "collect top 30 retweets"
#tweet_list = []
#for user in condensed_SN[0:30]:
tweets_array = np.array(sorted_tweets)

print "Preparing raw tweet data..."
test_dat = cv.transform(tweets_array)

## retrain classifier with optimized C parameter
logR = LogisticRegression(penalty = 'l2', C = Copt) # L2 Gaussian regularization
logR.fit(cv_transform, mini_train_labels)

sentiment_pred = logR.predict(test_dat)
probs = logR.predict_proba(test_dat)
print "Sample predictions using Logistic Regression (first 20)\n"
output = zip(sentiment_pred[0:30], tweets_array[0:30], probs[0:30])


print " Prediction (1= positive, 0 = negative) \t Tweet \t Posterior P()"
for predicted_label, tweet, probability in output:
    print predicted_label, "\t"+ tweet+ "\t\t %.2f" % max(probability)

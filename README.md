## Twitter Playground
Twitter data are a rich and fertile playground to run NLP analyses. Here, I stream twitter data containing '#NBAFinals2015' or '#Warriors', and store them first into a local MongoDB database.

1.1 Creating db_restT
Key files: TweetToMongo.py, MongoGetSet.py
https://s3.amazonaws.com/w205_hw3bucket/tweets-q1.json

TweetToMongo.py is an adaptation of the TweetSerializer class. It's used in MongoGetSet.py to extract tweets and push them to the MongoDB collection.

-1.2 Creating db_tweets
Key files: S3toMongo.py, FollowersToMongo.py
https://s3.amazonaws.com/w205_hw3bucket/tweets-q2.json
FollowersToMongo.py is an adaptation of the TweetSerializer class. It was intended to be written with more functionality, but ended up being extremely similar to TweetToMongo.py. It's used in S3toMongo.py to extract tweets from AWS and store them in db_tweets.

-2.1 Top 30 Retweets

Key files: getTop30.py, FollowersToMongo.py
sorted entries in db_tweets by retweet_count.
The first half of getTop30.py finds the top 30 users and their locations after extracting a sorted list from db_tweets.


-2.2 Lexical Diversity

Key files: LexicalDiversity.py, LDplot.py, dbrestT_LDplot2.png
Grab list of all users from db_restT using simple find() method from pymongo. To expedite the process, I only downloaded 500 tweets for each user before calculating the lexical diversity. All the text was preprocessed to remove stopwords and symbols. LexicalDiversity.py was used to extract and store the data. LDplot.py was used to load the stored lexical diversities and output them as a .png barplot (using matplotlib). The output figure is dbrestT_LDplot2.png

-2.3 List of Followers of top 30 retweeted users stored in db_followers
Key files: getTop30.py, unfollowed.py

Collected followers ids over 12 hour difference. Only grabbed the list of followers ids for the top 30 (as opposed to all the users) in db_restT. Also limited number of followers_ids to 40000. Tried to have larger time gap between data collections, but initially used api.followers which took much longer (300 followers' pages every 15 minutes)and was prone to crashing due to lag in stream processing.  Later on, used api.followers_ids, which was much faster and reliable. Unfollowed.py extracted the top 10 users from db_restT and matched the list of followers from each of the two collections of followers_ids data (db_followers and db_followers2). The output is simply a printed statement of results.

-2.4 Sentiment Analysis
Key files: SentimentAnalysis.py, sentiment_train_dat.py

Training data was taken from the University of Michigan sentiment analysis Kaggle competition page :https://inclass.kaggle.com/c/si650winter11/data.
Applied logistic regression from scikit-learn with L2 regularization and C parameter of 1000 as derived from GridSearchCV. The model trained with 99% accuracy. However, after reviewing the predictions with actual twitter data, it is apparent the model is not able to match as accurately sports related tweets. This is likely due to the training data which consisted of tweets about books (e.g. Da Vinci Code). Accuracy could probably improve after preprocessing the text to remove stopwords and non-english characters or symbols. A more representative training set could have been constructed with a subset of these tweets. For instance, labelling tweets with smiley face emojis as positive and frowning face emojis as negative could potentially create a more relevant training set.
-3
Key files: backups.py
https://s3.amazonaws.com/w205_hw3bucket/db_restT_backup_2015-07-20.json
https://s3.amazonaws.com/w205_hw3bucket/db_tweets_backup_2015-07-20.json

The backups.py file contains two functions, one that creates backups in S3 and another that loads from S3 back into mongodb. The reloading function has the backup files hardwired into a list and would be implemented within a for loop similar to the one used for the backup-to-s3 function.

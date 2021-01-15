# Light-weight data interchange format.
import json
# Python client for the official Twitter API.
import tweepy
# Sequence of characters that forms a search pattern.
import re
# Python library processing textual data.
from textblob import TextBlob
# Catches any errors assosiated with Tweepy.
from tweepy import TweepError
# Creates a connection to the MySQL server.
import mysql.connector
# Catches any errors assosiated with Tweepy.
from mysql.connector import Error
# Parses most kwown formats to represent a date and/or time.
from dateutil import parser
# Import graphs from the Graph.py
import Graphs


class TwitterClient(object):
    """
    A generic Twitter class for sentiment analysis
    """
    def __init__(self):
        
        pass

    def clean_tweet(self, tweet): 
        """
        Function to clean tweet text by removing links, special characters using 
        the regex library. 
        """
        tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 
        return tweet
    
    def get_tweet_sentiment(self, tweet): 
        """
        Function to classify sentiment of passed tweet 
        using TextBlob library. 
        """
        # Create TextBlob object of passed tweet text.
        analysis = TextBlob(self.clean_tweet(tweet)) 
        # Set sentiment.
        if analysis.sentiment.polarity > 0: 
            #print(analysis.sentiment.polarity, 'positive')
            return 'positive'
        elif analysis.sentiment.polarity < 0:
            #print(analysis.sentiment.polarity, 'negative')
            return 'negative'
        else:
            #print('neutral')
            return 'neutral'


TCl = TwitterClient()


def store_data(user_id, user, created_at, category, tweet, tweets_no, retweets_no, location, followers, hashtags, polarity, subjectivity, sentiment):
    """
    Function to connect to MySQL database and insert twitter data.
    """
    try:
        # Avoid inserting tweets with no category
        if category != '':
            db = mysql.connector.connect(host='localhost', database = 'twitter', user='root', password = '', charset = 'utf8')
            if db.is_connected():
                print("A new tweet has been inserted in the database: ",'"{}"'.format(tweet))
                print()
                mycursor = db.cursor()
                query = "INSERT INTO social (user_id, user, created_at, category, tweet, tweets_no, retweets_no, location, followers, hashtags, polarity, subjectivity, sentiment) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                mycursor.execute(query, (user_id, user, created_at, category, TCl.clean_tweet(tweet), tweets_no, retweets_no, location, followers, hashtags, polarity, subjectivity, TCl.get_tweet_sentiment(tweet)))
                db.commit()
            mycursor.close()
            db.close()   
    except Error as e:
        print(e)       
       
     
    return


class StreamListener(tweepy.StreamListener):
    """
    Tweepy class to access Rwitter API.
    """

    def on_connect(self):
        print("You are connected to the Twitter API")

    def on_error(self, status_code):
        print("An error occured: " + repr(status_code))
        return False
    
    def on_data(self, data):
        """
        Function to read tweet data as Json and
        extracts the desirable data.
        """   
        try:
            data = json.loads(data)
            # To avoid collecting retweets.     
            if data['in_reply_to_status_id'] is None: 
                return True 
                
            if 'text' in data:
                user_id = data['id_str']
                user = data['user']['screen_name']
                created_at = parser.parse(data['created_at'])                    
                tweet = TCl.clean_tweet(data['text'])
                
                # Create empty list to store the category for each tweet.    
                alist = []      
                category = ''
                for i in ['WHATSAPP', 'SNAPCHAT','INSTAGRAM']:
                    if i in tweet.upper():
                        alist.append(i)
                        category = ' '.join([str(elem) for elem in alist])
                            
                tweets_no = data['user']['statuses_count']
                retweets_no = data['retweet_count']
                location = data['user']['location']
                followers = data['user']['followers_count']
                # Create an empty list to store the hashtags for each tweet.
                hashtags = []     
                for hashtag in data['entities']['hashtags']:
                    hashtags.append(hashtag['text'])
                # Convert list to a string.     
                hashtags = ' '.join(hashtags)  
                analysis = TextBlob(TCl.clean_tweet(tweet))
                polarity = analysis.sentiment.polarity
                subjectivity = analysis.sentiment.subjectivity
                sentiment = TCl.get_tweet_sentiment(tweet)
            # Insert collected data into MySQL database.
            store_data(user_id, user, created_at, category, tweet, tweets_no, retweets_no, location, followers, hashtags, polarity, subjectivity, sentiment)
           
        except Exception as e:
            print(e)
            

def main():
    
    # Keys and tokens fron the Twitter Dev Console.
    with open('credentials.json', 'r') as f:
        creds = json.load(f)
        consumer_key = creds["consumer_key"]
        consumer_secret = creds["consumer_secret"]
        access_token = creds["access_token"]
        access_token_secret = creds["access_token_secret"]
    
    try:
        # Try authentification to access Twitter.
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api =tweepy.API(auth, wait_on_rate_limit = True,)
    except Exception as e:
            raise TweepError(e)
            
    # Create instance of Streamlistener.
    listener = StreamListener(api)
    stream = tweepy.Stream(auth, listener = listener)
    
    # Choose the words we want to trach in tweets. 
    track = ['WHATSAPP', 'SNAPCHAT','INSTAGRAM']
    # Choose the filter we want to use. (Choosing English language)
    stream.filter(track = track, languages = ['en'])
    
    
if __name__== '__main__':
    """
    We call the main function.
    """
    main()  
                        
                
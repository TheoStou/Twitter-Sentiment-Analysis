# Twitter-Sentiment-Analysis
(Measure the public's sentiment based on their tweets concerning a specific topic.)


Twitter sentiment analysis is defined as the automated procedure of distinguishing and extracting personal information that underlies a text. This information may contain an opinion, an assessment, or even an emotional expression about a topic or a matter. Primarily, one of the most common types of sentiment analysis used, is that of the polarity score, classifying an expression as “positive”, “negative” or “neutral”. The scope of this report is to develop a sentiment analysis based on Twitter, gather user information about three substantial social media platforms “WhatsApp”, “Snapchat” and “Instagram” and provide the results of this analysis. To fulfill our purpose, we start by creating a developer account on Twitter, so as to have access to our API key, as well as a database table where we can store the desired data. Then we use python to preprocess(clean) the unstructured tweets to prepare them for the stage of sentiment analysis. With the help of the TextBlob python's library we implement a sentiment analysis, categorizing the tweets as positive, negative, or neutral.

Table of Contents
=================

* [Basic Libraries](#basic-libraries)
* [Methodology](#methodology)
    * [1. Create a Twitter developer account.](#create-a-twitter-developer-account)
    * [2. Collect and store tweets into a database.](#2.-collect-and-store-tweets-into-a-database.)
    * [3. Pre-process tweets to prepare for the sentiment analysis.](#3.-pre-process-tweets-to-prepare-for-the-sentiment-analysis.)
    * [4. Apply sentiment analysis.](#4.-apply-sentiment-analysis.)
    * [5. Visualize the results.](#5.-visualize-the-results.)
* [References](#references)



## Basic Libraries
| **Library** | **Description** |
| :--- | :--- |
| tweepy | Access Twitter API. |
| re | Alternative regular expression module. |
| mysql.connector | Communication with MySQL server. |
| pandas | Handle data structures and data analysis tool. |
| numpy | Process numbers, strings, records and objects. |
| matplotlib.pyplot | Implement plots. |
| seaborn | Python data visualization library based on matplotlib. |
| json | Provide decoding/encoding. |


## Methodology
1. Create a Twitter developer account.
2. Collect and store tweets into a database.
3. Pre-process tweets to prepare for the sentiment analysis.
4. Apply sentiment analysis.
5. Visualize the results.


### 1. Create a Twitter developer account.
For this analysis, it is significant to apply for a Twitter developer account. The Twitter developer portal is a set of self-service tools that we can manage our access to the APIs with a set of credentials that we must pass with requests. Therefore, an app was created, giving access to some credentials such as the API key, the API secret key as well as the access tokens, and the access token secret- allowing to proceed with the authentication of the program.


### 2. Collect and store tweets into a database.
Several tweets were collected regarding  the aforementioned social media platforms, Instagram, Snapchat, and WhatsApp, using directly Twitter API. For this specific occasion, MySQL workbench was utilized to construct and manage the database. The total amount of the collected tweets were in English language and were stored in a new created table named “social”. The structure of the (table) is demonstrated down below.

| **Columns** | **Description** |
| :--- | :--- |
| user_id | The user identification number. |
| user | Username of the account wrote the tweet. |
| created_at | Date and time when tweet exactly written. |
| category | Indicates the social media platform in which the tweet refers to. |
| tweet | The main text of the tweet. |
| tweet_no | The number of tweets that the specific twitter account has posted altogether. |
| retweet_no | The number of the retweets that the tweet post has. |
| location | Information about the location of the user that made a tweet post. |
| followers | The number of followers that the specific twitter account has. |
| hashtags | Hashtags associated with the tweet post. |
| polarity | Occurs from the sentiment analysis, providing how positive or negative a tweet is. It takes numbers between -1.0 and 1.0. |
| subjectivity | Classifies a tweet as opinionated or not. It takes numbers between 0 and 1. |
| sentiment | The outcome of sentiment analysis based on polarity. Classifies a tweet as “positive”, “negative” or “neutral”. |


### 3. Pre-process tweets to prepare for the sentiment analysis.
Data cleansing constitutes a crucial step for an accurate sentiment analysis since tweets often contain many abbreviations, punctuations, URLs, and other characters that can make the sentiment analysis a challenging task. “clean_tweet” function is utilized in order to deal with these mentioned cases.

```ruby
    def clean_tweet(self, tweet): 
        tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 
        return tweet
```


### 4. Apply sentiment analysis.
Python's library "TextBlob" was used to conduct the classification of the collected tweets. "TextBlob" defines is mainly utilized in textual data and provide us with two float scores, polarity, and subjectivity. The former of the two scores is analyzed to classify a tweet as positive (polarity > 0.0), negative (polarity < 0.0), or neutral (polarity equals to 0.0), whereas the latter of the two scores, subjectivity, characterizes a tweet either as a subjective opinion or as an objective fact. The  function "get_tweet_sentiment" is used to measure the sentiment of a given tweet. 

```ruby
    def get_tweet_sentiment(self, tweet): 
        analysis = TextBlob(self.clean_tweet(tweet)) 
        # Set the sentiment.
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity < 0:
            return 'negative'
        else:
            return 'neutral'
```


### 5. Visualize the results.
Data visualization is a substantial part of any analysis. Therefore a representation of data will help us understand any possible relationship between the different variables. The Graphs.py file provides various plots (categorical plots, density plots, times series plots, a bar chart, a word cloud). An example of two density plots regarding the polarity and the subjectivity is demonstrated down below. 

<p align="center">
  <img width="500" height="370" src="https://user-images.githubusercontent.com/74372152/104822178-611bc980-5849-11eb-8249-d29d11a804f5.png">
</p>
<p align="center"> Density Plot of Polarity. <p align="center">

<p align="center">
  <img width="500" height="370" src="https://user-images.githubusercontent.com/74372152/104822241-c53e8d80-5849-11eb-814b-4e60f3d9b87b.png">
</p>
<p align="center"> Density Plot of Subjectivity. <p align="center">

## References
[1] https://textblob.readthedocs.io/en/dev/quickstart.html#sentiment-analysis <br/>
[2] https://dl.acm.org/doi/10.1145/3209281.3209313 <br/>
[3] https://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/

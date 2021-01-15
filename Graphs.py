# Data visualization library based on matplotlib.
import seaborn as sns
# Creates a connection to the MySQL server.
import mysql.connector
# A plotting library.
import matplotlib.pyplot as plt
# Library to make a word cloud.
from wordcloud import WordCloud
# Library for data manipulation and analysis.
import pandas as pd
import matplotlib as mpl


def categ_plot(x, y):
    """
    Categorical plots for WhatsApp, Snapchat and Instagram 
    based on tweet count regarding sentiment analysis.
    """
    names = ['negative', 'neutral', 'positive']
    values = x
    plt.figure(figsize=(10, 3))
    plt.subplot(131)
    plt.bar(names, values)
    plt.subplot(132)
    plt.scatter(names, values)
    plt.subplot(133)
    plt.plot(names, values)
    plt.suptitle(y)
    plt.show()


def polar_graph():
    """
    A density plot for polarity.
    """
    # Connect to the database named twitter.
    db=mysql.connector.connect(host='localhost', user='root', password='', db='twitter', charset="utf8")
    cursor = db.cursor()
    # Collect polarity data for each social media app
    cursor.execute("select polarity from social where category = 'WHATSAPP';")
    whatsapp = [item[0] for item in cursor.fetchall()]
    cursor.execute("select polarity from social where category = 'SNAPCHAT';")
    snapchat = [item[0] for item in cursor.fetchall()]
    cursor.execute("select polarity from social where category = 'INSTAGRAM';")
    instagram = [item[0] for item in cursor.fetchall()]
    # Draw density plot 
    sns.kdeplot(whatsapp, shade=True, color="g", label="WhatsApp")
    sns.kdeplot(snapchat, shade=True, color="y", label="Snapchat")
    sns.kdeplot(instagram, shade=True, color="fuchsia", label="Instagram")
    plt.suptitle('Polarity of the three Social Media Messaging apps')
    plt.show()


def subj_graph():
    """
    A density plot for subjectivity.
    """
    # Connect to the database named twitter.
    db=mysql.connector.connect(host='localhost', user='root', password='', db='twitter', charset="utf8")
    cursor = db.cursor()
    # Collect subjectivity data for each social media app
    cursor.execute("select subjectivity from social where category = 'WHATSAPP';")
    whatsapp = [item[0] for item in cursor.fetchall()]
    cursor.execute("select subjectivity from social where category = 'SNAPCHAT';")
    snapchat = [item[0] for item in cursor.fetchall()]
    cursor.execute("select subjectivity from social where category = 'INSTAGRAM';")
    instagram = [item[0] for item in cursor.fetchall()]
    # Draw density plot
    sns.kdeplot(whatsapp, shade=True, color="g", label="WhatsApp")
    sns.kdeplot(snapchat, shade=True, color="y", label="Snapchat")
    sns.kdeplot(instagram, shade=True, color="fuchsia", label="Instagram")
    plt.suptitle('Subjectivity of the three Social Media Messaging apps')
    plt.show()
    

def Timeseries_graph(df, brand):
    """
    Time series graph for WhatsApp, Snapchat and Instragram. Number of  positive,
    negative and neutral tweets over a period.
    """
    # UTC for date time at default.
    df['created_at'] = pd.to_datetime(df['created_at'])
    print("Candidates Negative Tweets Monitor: ")
    for index, tweets in df[df['sentiment'] == 'negative'].iterrows():
        print("  " +str(tweets[2]) + "  " + tweets[1])

    # Clean and transform data to enable time series.
    result = df.groupby([pd.Grouper(key='created_at', freq='80min'), 'sentiment']).count() \
            .unstack(fill_value=0).stack().reset_index()
    result['created_at'] = pd.to_datetime(result['created_at']).apply(lambda x: x.strftime('%m-%d %H:%M'))

    # Plot Line Chart for monitoring brand awareness on Twitter.
    mpl.rcParams['figure.dpi']= 200
    plt.figure(figsize=(16, 8))
    sns.set(style="darkgrid")
    ax = sns.lineplot(x = "created_at" ,y="user_id", hue='sentiment', data=result,\
                      palette=sns.color_palette(["#FF5A5F","#484848", "green"]))
    ax.set(xlabel='Time Series in UTC', ylabel="Number of {} tweets".format(brand))
    plt.legend(title='Sentiment Analysis over Time', loc='upper left', labels=['Negative', 'Neutral', 'Positive'])
    sns.set(rc={"lines.linewidth": 1})
    plt.show()
    
    
def barplot(populars):
    """
    A simple bar plot that shows the most popular users (users with the most followers).
    """
    # append data from the dict populars in dataframe
    df = pd.DataFrame({'User': list(populars.keys()), 'Followers': list(populars.values())})
    df['User'] = df.index
    plt.figure(figsize=(16,5))
    # Draw barplot
    ax = sns.barplot(data = df, x = "User", y = "Followers")
    ax.set(ylabel = "Followers")
    ax.set_xticklabels(populars.keys())
    plt.show()


def wordcloud():
    """
    A plot providing the most frequent words in the tweets text.
    """
    # Connect to the database named twitter.
    db=mysql.connector.connect(host='localhost', user='root', password='', db='twitter', charset="utf8")
    cursor = db.cursor()
    # Collect tweet text
    cursor.execute("select tweet from social")
    tweet = [item[0] for item in cursor.fetchall()]
    # Draw worcloud
    wordcloud = WordCloud(max_words=1000, margin=10, background_color='white',scale=3, relative_scaling = 0.5, width=500, height=400,random_state=1).generate(' '.join(tweet))
    plt.figure( figsize=(20,10), facecolor='k')
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.title("Twitter sentiment analysis")
    plt.show()

# Connect to the database named twitter.
db=mysql.connector.connect(host='localhost', user='root', password='', db='twitter', charset="utf8")
cursor = db.cursor()
cursor.execute("select count(sentiment) from social where category = 'WHATSAPP' group by sentiment;")
whatsapp = [item[0] for item in cursor.fetchall()]
cursor.execute("select count(sentiment) from social where category = 'SNAPCHAT' group by sentiment;")
snapchat = [item[0] for item in cursor.fetchall()]
cursor.execute("select count(sentiment) from social where category = 'INSTAGRAM' group by sentiment;")
instagram = [item[0] for item in cursor.fetchall()]

categ_plot(whatsapp,'Number of Tweets for WhatsApp')
categ_plot(snapchat,'Number of Tweets for Snapchat')
categ_plot(instagram,'Number of Tweets for Instagram')


polar_graph()
subj_graph()

# Connect to the database named twitter.
db = mysql.connector.connect(host='localhost', database = 'twitter', user='root', password = '', charset = 'utf8')
whatsapp = pd.read_sql("SELECT user_id, tweet, created_at, sentiment, location FROM social WHERE category = 'WHATSAPP'", con=db)
snapchat = pd.read_sql("SELECT user_id, tweet, created_at, sentiment, location FROM social WHERE category = 'SNAPCHAT'", con=db)
instagram = pd.read_sql("SELECT user_id, tweet, created_at, sentiment, location FROM social WHERE category = 'INSTAGRAM'", con=db)


Timeseries_graph(whatsapp, 'WHATSAPP')
Timeseries_graph(snapchat, 'SNAPCHAT')
Timeseries_graph(instagram, 'INSTAGRAM')


# Connect to the database named twitter.
db=mysql.connector.connect(host='localhost', user='root', password='', db='twitter', charset="utf8")
cursor = db.cursor(dictionary = True)
# Create a dict named popular. 
populars = {}
# This query returns a list of the users who have followers more than 140000 followers in the db
cursor.execute("select user, followers from social where followers > 140000")
# Assign user as key in dict populars and followers as value.
for row in cursor:
    user = row["user"]
    followers = row["followers"]
    populars[user] = followers

user = populars.keys()
followers = populars.values()
barplot(populars)


wordcloud()



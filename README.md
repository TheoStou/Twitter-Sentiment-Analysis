# Twitter-Sentiment-Analysis
(Measure the public's sentiment based on their tweets concerning a specific topic.)


Twitter sentiment analysis is defined as the automated procedure of distinguishing and extracting personal information that underlies a text. This information may contain an opinion, an assessment, or even an emotional expression about a topic or a matter. Primarily, one of the most common types of sentiment analysis used, is that of the polarity score, classifying an expression as “positive”, “negative” or “neutral”. The scope of this report is to develop a sentiment analysis based on Twitter, gather user information about three substantial social media platforms “WhatsApp”, “Snapchat” and “Instagram” and provide the results of this analysis. To fulfill our purpose, we start by creating a developer account on Twitter, so as to have access to our API key, as well as a database table where we can store the desired data. Then we use python to preprocess(clean) the unstructured tweets to prepare them for the stage of sentiment analysis. With the help of the TextBlob python's library we implement a sentiment analysis, categorizing the tweets as positive, negative, or neutral.


## Methodology
1. Create a Twitter developer account.
2. Collect and store tweets into a database.
3. Pre-process tweets to prepare for the sentiment analysis.
4. Apply sentiment analysis.
5. Evaluate the results.


## 1. Create a Twitter developer account.
For this analysis, it is significant to apply for a Twitter developer account. The Twitter developer portal is a set of self-service tools that we can manage our access to the APIs with a set of credentials that we must pass with requests. Therefore, an app was created, giving access to some credentials such as the API key, the API secret key as well as the access tokens, and the access token secret- allowing to proceed with the authentication of the program.


## 2. Collect and store tweets into a database.
Several tweets were collected regarding  the aforementioned social media platforms, Instagram, Snapchat, and WhatsApp, using directly Twitter API. For this specific occasion, MySQL workbench was utilized to construct and manage the database. The total amount of the collected tweets were in English language and were stored in a new created table named “social”. The structure of the (table) is demonstrated down below.

| Columns | Description |
| :--- | :--- |
| user_id | The user identification number. |
| user | Username of the account wrote the tweet. |



import nltk
import os

# Now we will have the main part - w will not downloading the vader_lexical package
# we can directly use it form the current working directory - and specify as a path to be used

# This line tells NLTK where to look for its downloaded data files (like vader_lexicon)
# os.getcwd() - /Users/prathamsharma/scoreAnalyzer
# 'nltk_data' - Folder name where NLTK resources are stored
# os.path.join(os.getcwd(), 'nltk_data') - Safely combines paths
# nltk.data.path.append(...) - Adds a new directory to NLTK’s search list, tells the NLTK Also check this folder when looking for directory
nltk.data.path.append(os.path.join(os.getcwd(), 'nltk_data'))

# Import the model SentimentIntensityAnalyzer from the vader
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Then create the object for the SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

# Here we have defined the analyse_sentiment() function and in this we are depicting the all the posts with posts variable
# Creating the posts variable pointing to the posts using for analysing the sentiment
# Analyse sentiment API will be working with each post and we will get the scores and classification
def analyse_sentiment(posts):
    results = [] # the result of each and every post will be saved in the results in array format
    for post in posts:
        # get the sentiments scores
        # here the polarity_scores() will take the content and then we can go for compound scoring
        sentiment_score = sia.polarity_scores(post['content'])['compound']

        # Classiy sentiment based on the compound score
        sentiment = 'POSITIVE' if sentiment_score >=0 else 'NEGATIVE'

        #append the results - below dictonary will be created and then added to the results array
        results.append({
            "title": post['title'],
            "content": post['content'],
            "sentiment": sentiment,
            "score": sentiment_score
        })
    return results
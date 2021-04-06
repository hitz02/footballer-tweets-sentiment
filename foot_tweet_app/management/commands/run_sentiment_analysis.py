print('Importing Utilities')
from django.core.management import BaseCommand
from foot_tweet_app.models import Tweets, Twitter_Handles, Sentiment
import pandas as pd
import numpy as np
import preprocessor as p #tweet preprocessor library
import emoji
import re
import json
from textblob import TextBlob #library for Finding sentiments
import sys
from tqdm import tqdm

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

print('Reading data')
df = pd.DataFrame.from_records(Tweets.objects.all().values())

#Only extract english tweets
en_tweet_df = df[df['language']=='en'] #English tweets


#setting options to remove urls and mentions from tweet
p.set_options(p.OPT.URL,p.OPT.MENTION)


# A function to clean the tweet using the tweet preprocessor and demojize (convert emoji to text)
def clean_tweet(tweet):
    return emoji.demojize(p.clean(tweet))


#Read docstring inside function
def get_tweet_sentiment(tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(clean_tweet(tweet))

        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'


print('Cleaning Data')
#Apply clean tweet function on tweets and create new column of cleaned tweets
en_tweet_df['cleaned_tweet'] = en_tweet_df.apply(lambda row:clean_tweet(row['tweet']),axis=1)


print('Fetching Sentiments')
#Apply get tweet sentiment function on tweets and create new column of sentiment
en_tweet_df['sentiment'] = en_tweet_df.apply(lambda row:get_tweet_sentiment(row['cleaned_tweet']),axis=1)

en_tweet_df = en_tweet_df[['player_name','screen_name','created_at','cleaned_tweet','covid_time','sentiment']]

class Command(BaseCommand):
    help = 'Perform sentiment analysis on tweets and load in database'

    def handle(self, *args, **kwargs):

        self.stdout.write("Starting to delete previous Sentiments from database")

        t = Sentiment.objects.all()
        t._raw_delete(t.db)

        self.stdout.write("Previous Sentiments Deleted Successfully")

        json_list = json.loads(json.dumps(list(en_tweet_df.T.to_dict().values())))

        self.stdout.write("Starting to load new Sentiments in database")

        for dic in tqdm(json_list):
            Sentiment.objects.get_or_create(**dic)

        self.stdout.write("Sentiments Loaded Successfully")

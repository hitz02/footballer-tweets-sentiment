import csv
from django.core.management import BaseCommand
from foot_tweet_app.models import Tweets, Twitter_Handles
import tweepy
import pandas as pd
from tqdm import tqdm
import time
from datetime import datetime
import sys
import json

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

print('Performing Twitter Authentication')
# Authenticate to Twitter

auth = tweepy.OAuthHandler(os.environ.get('API_KEY'),os.environ.get('API_KEY_SECRET'))

auth.set_access_token(os.environ.get('ACCESS_TOKEN'),os.environ.get('ACCESS_TOKEN_SECRET'))

api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

#Function to get tweets given a screen_name
def get_tweets(sc_name):
    tweets = api.user_timeline(screen_name=sc_name,
                               # 200 is the maximum allowed count keeping 100 for now
                               count=100,
                               include_rts = False,
                               # Necessary to keep full_text
                               # otherwise only the first 140 words are extracted
                               tweet_mode = 'extended'
                               )
    return tweets

print('Reading Player list file')
data = pd.DataFrame.from_records(Twitter_Handles.objects.all().values())

#Remove @ symbol from the handle as it is not required in the next steps
data['twitter_handle'] = data['twitter_handle'].str.replace('@','')

data['player_name'] = data['player_name'].str.strip()

#Store the names in a variable
players_handles = data.twitter_handle.values
player_names = data.player_name.values


#Create an empty list to store tweet data
final_list = []

print('Fetching tweets for each players')
#For each player -> 1. get the tweets 2. extract required elements 3. append as a list in final_list
for sc_name,p_name in tqdm(zip(players_handles,player_names)):
    try:
        time.sleep(1) #just to keep some time gap between api calls and avoid any error
        tweets = get_tweets(sc_name)
        for info in tweets:
            final_list.append([info.user.id,p_name,info.user.screen_name,info.created_at,info.full_text,info.lang])
    except tweepy.TweepError:
        # print('Error')
        pass

#Store the final_list as a dataframe
final_df = pd.DataFrame(final_list,columns=['handle_id','player_name','screen_name','created_at','tweet','language'])

#Choose the covid date to create binary flag for -> before after covid flag
covid_date = pd.to_datetime('31-12-2019')

#Create binary covid time flag using the the above created date
final_df['covid_time'] = final_df.apply(lambda row:1 if row['created_at']>covid_date else 0,axis=1)

final_df['created_at'] = final_df['created_at'].dt.strftime('%Y%m%d%H%M%S')


class Command(BaseCommand):
    help = 'Load tweets into the database'

    def handle(self, *args, **kwargs):

        self.stdout.write("Starting to delete previous Tweets from database")
        t = Tweets.objects.all()
        t._raw_delete(t.db)
        self.stdout.write("Previous Tweets Deleted Successfully")

        json_list = json.loads(json.dumps(list(final_df.T.to_dict().values())))

        self.stdout.write("Starting to load new Tweets in database")

        for dic in tqdm(json_list):
            Tweets.objects.get_or_create(**dic)

        self.stdout.write("Tweets Loaded Successfully")
from django.db import models

# Create your models here.

class Twitter_Handles(models.Model):
    player_name = models.CharField(max_length=150)
    twitter_handle = models.CharField(max_length=100)
    team_name = models.CharField(max_length=150)
    player_position = models.CharField(max_length=10,default='')

class Tweets(models.Model):
    handle_id = models.BigIntegerField(default=0)
    player_name = models.CharField(max_length=150)
    screen_name = models.CharField(max_length=150,default='NA')
    created_at = models.CharField(max_length=100)
    tweet = models.CharField(max_length=1000)
    language = models.CharField(max_length=5)
    covid_time = models.IntegerField(default=9)

class Sentiment(models.Model):
    player_name = models.CharField(max_length=150)
    screen_name = models.CharField(max_length=150)
    created_at = models.CharField(max_length=100)
    cleaned_tweet = models.CharField(max_length=1000)
    covid_time = models.IntegerField(default=9)
    sentiment = models.CharField(max_length=15)
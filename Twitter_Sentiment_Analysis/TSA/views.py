from django.shortcuts import render
from django.http import HttpResponse
from . import models
import tweepy
from textblob import TextBlob
import csv
import datetime

# Create your views here.
def home(request):
    return render(request,'home.html',{'name':'Rajesh'})

def add(request):
    consumer_key        = request.GET["consumer_key"]
    consumer_secert_key = request.GET["consumer_secert_key"]
    access_token        = request.GET["access_token"]
    access_token_secret = request.GET["access_token_secret"]
    topic               = request.GET["topic"]

    auth = tweepy.OAuthHandler(consumer_key,consumer_secert_key)
    auth.set_access_token(access_token,access_token_secret)
    
    api = tweepy.API(auth)
    
    public_tweets = api.search(q=topic,count=100)
    
    all_tweets = []
    
    for tweet in public_tweets:
        tweet_obj = models.Tweets()
        tweet_obj.tweet = tweet.text
        
        # Ananlyzing the tweet
        analysis = TextBlob(tweet.text)
        
        tweet_obj.polarity = analysis.sentiment.polarity
        tweet_obj.subjectivity = analysis.sentiment.subjectivity
        
        if tweet_obj.subjectivity > 0.5:
            if tweet_obj.subjectivity == 1.0:
                tweet_obj.type_of_tweet = 'Very Subjective'
            else:
                tweet_obj.type_of_tweet = 'Subjective'
        
        if tweet_obj.subjectivity < 0.5:
            if tweet_obj.subjectivity == 0.0:
                tweet_obj.type_of_tweet = 'Very Objective'
            else:
                tweet_obj.type_of_tweet = 'Objective'        
        
        all_tweets.append(tweet_obj)
        
    return render(request, 'result.html',{'all_tweets':all_tweets})
from django.db import models

# Create your models here.

class Tweets:
    tweet: str
    polarity: float
    subjectivity: float
    type_of_tweet: str
    style: str
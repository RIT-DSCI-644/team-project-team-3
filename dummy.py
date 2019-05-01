import csv
import pandas as pd
import numpy as np
from helper_functions import get_average_sentiment, get_top_retweeted, get_most_conservative, get_most_liberal, get_sentiment_frequency, get_most_positive, get_most_negative
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sentiment import *

vader = SentimentIntensityAnalyzer()

stopword = pd.read_csv('stopwords.csv')
stopword = stopword['a']
stopword = set(stopword)
#print(stopword)
trump=pd.read_csv('trump_raw.csv')
clinton=pd.read_csv('clinton_raw.csv')
congress=pd.read_csv('congress_raw.csv')

#get_average_sentiment(clinton)
get_top_retweeted(clinton, 3)
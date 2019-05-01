#%% [markdown]
# As of Saturday March 23:
# 
# To run this program you need the three datasets and the stopwords file in the same directory as this program.
# 
# The program does the following:
# Puts the three tweet datasets into dataframes.
# Performs sentiment analysis on the tweets using the nltk.vader tool.   This is a lexicon based sentiment analysis trained using social media sources, so we assume it is somewhat applicable.  The analysis is added to the dataframes in two forms, the overall score from -1 to 1 showing magnitude of sentiment, as well as an integer score of -1,0,1 (meaning negative positive neutral) showing only direction of sentiment.  Called Vader_Score and Trinary_Score.
# 
# A shortcoming of this analysis as is is that any new slang terms or created words or hashtags likely won't be interpretted by the classifier so they'll be simply counted as neutral.  Might miss SOME of the data.
# 
# March 24: Hand classified some data for test of accuracy of classifier.  Got about 70% accuracy over fifty random data points from the congress dataset.  Seems good enough for our purposes.
#           Auto exports the sentiment dataframes to program directory - for use by other programs in the directory

#%%
#import numpy as np
import pandas as pd
import collections
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import csv
import math
import random


#%%
###Downloads the lexicon used for sentiment anlysis.  Can comment out after run once.
nltk.downloader.download('vader_lexicon')

#%% [markdown]
# Import the datasets and turn into DataFrames.

#%%
trump=pd.read_csv('trump_raw.csv')
clinton=pd.read_csv('clinton_raw.csv')
congress=pd.read_csv('congress_raw.csv')

#%% [markdown]
# Stopwords for basic text cleaning for wordclouds

#%%
stopwords = []
file2=open('stopwords.csv', encoding='utf8')   #file of stopwords from another project...may need to make this file bigger.
for stopword in file2.read().split():
    stopword = stopword.replace('"','')
    stopwords.append(stopword)
file2.close()

# Wordcloud Function
#%%
#####Setting up wordcloud creation.   Takes a list of text entries that we create later.
###Second argument is size of the cloud you want returned.  default is top 20 words
def make_cloud(words, num=20):
    wordcount={}
    for line in words:
        for word in line.split():
            if word in stopwords:
                pass
        
            elif word not in wordcount:
                wordcount[word] = 1
            else:
                wordcount[word] += 1
    
    d = collections.Counter(wordcount)
        
    for word, count in d.most_common(num):
        print(word, ": ", count)
    print("\n")

#%% [markdown]
# Grab All of the text from the tweets from a given DataFrame.  For use with wordcloud generation.

#%%
def grab_text(df):
    cw =[]
    df = df["text"]   #Grab just the fourth column
        
    for x in df.index:    #Iterate over the valid indicies. Need this since congresslib/con are partials. 
        temp=str(df[x])
        temp.strip()                  ##Cleans up the text of junk characters
        temp=temp.replace('.','')  #stripping out common punctuation so words ending with commas and periods don't count as two different words.
        temp=temp.replace(',','')
        temp=temp.replace('“','')
        temp=temp.replace('”','')
        temp=temp.replace('&amp','')
        temp=temp.replace(';','')
        temp=temp.replace('-',' ')
        temp=temp.lower()
        cw.append(temp)
    return cw


#%%
###Example of word cloud.  Not sure if we'll use this.  We may use its helpr functions if we build our own 
###classifier...


make_cloud(grab_text(trump))


#%%



#%%


#%% [markdown]
# Sentiment Analysis Stuff follows.

#%%
###The analyzer.  returns a number between [-1,1] with -1 being very negative and 1 being very positive.
###Use the compound output as the overall sentiment. (it's some kind of combination of all three attributes)
vader = SentimentIntensityAnalyzer()


#%%
###Gives a Trinary Poisitive/Negative/Neutral answer.  Will be useful for strict counts of positive/negative/neutral.

def vader_polarity(text):
    """ Transform the output to a binary 0/1 result """
    score = vader.polarity_scores(text)
    if score['pos'] > score['neg']:
        x=1
    elif score['pos'] < score['neg']:
        x=-1
    else:
        x=0
    return x


#%%
##Example of the sentiment analyzer and the trinary classifications
##Shows a tweet, the vader nltk.vader analysis, and the trinary classification.

x1=trump['text'][0]
print(x1)
print(vader.polarity_scores(x1))
print(str(vader_polarity(x1))+"\n")
x2=trump['text'][5]
print(x2)
print(vader.polarity_scores(x2))
print(str(vader_polarity(x2))+"\n")
x3=trump['text'][4]
print(x3)
print(vader.polarity_scores(x3))
print(vader_polarity(x3))

#%% [markdown]
# Note that the output from vader gives 4 numbers.  we should use the compound number.  It is calculated using some sort of squishing formula behind the scenes... it's exact function is not important to this analysis and the number should work fine.
# 
#%% [markdown]
# Function for analyzing sentiment of all tweets and appending to datasets.

#%%
def grab_data_sentiment(df):
    Vader_Score = []
    Trinary_Score = []
    df = df["text"]   #Grab just the fourth column
        
    for x in df.index:    #Iterate over the valid indicies. Need this since congresslib/con are partials. 
        temp=str(df[x])
        vad_score=vader.polarity_scores(temp)['compound']
        trin_score=vader_polarity(temp)
        
        Vader_Score.append(vad_score)
        Trinary_Score.append(trin_score)
    return Vader_Score, Trinary_Score


#%%
y,z=grab_data_sentiment(trump)
trump.insert(0,'Vader_Score',y)
trump.insert(0,'Trinary_Score',z)

y,z=grab_data_sentiment(clinton)
clinton.insert(0,'Vader_Score',y)
clinton.insert(0,'Trinary_Score',z)

##This one takes a while, large dataset...
y,z=grab_data_sentiment(congress)
congress.insert(0,'Vader_Score',y)
congress.insert(0,'Trinary_Score',z)

#%% [markdown]
# Showing the dataframe with the sentiment scores inserted.

#%%
trump.head()

#%% [markdown]
# create DFs for separated congress for basic analysis

#%%
pd.to_numeric(congress['dw_score'])  ##negatives were parsing as strings
lib_filter=congress['dw_score']<0
con_filter=congress['dw_score']>0
congress_lib=pd.DataFrame(congress[lib_filter])  ##Creating copies to get rid of indexing issues.
congress_con=pd.DataFrame(congress[con_filter])


#%%
congress_lib.head()

#%% [markdown]
# Save copies of the files for use in main program.

#%%
trump.to_csv('trump_sentiment.csv', header=True)
clinton.to_csv('clinton_sentiment.csv', header=True)
congress.to_csv('congress_sentiment.csv', header=True)
congress_lib.to_csv('congress_lib_sentiment.csv', header=True)
congress_con.to_csv('congress_con_sentiment.csv', header=True)

#%% [markdown]
# Rough validity of Sentiment Checker.

#%%
random.seed(0)  ###Don't change.  Human input based on the random choices from this...  "chrissentiment"
congressrand=congress
randindexlist=[]
for x in congressrand.index:
    randindexlist.append(x)
random.shuffle(randindexlist)
testlist=randindexlist[:50]
#testlist=randindexlist[:20]
###Originally ran on 20 points.  upped to 50 for better confidence in results
testlist=sorted(testlist)
testlist
pd.set_option('display.max_colwidth', -1)
congressrand=congressrand.iloc[testlist]
congressrand['text']


#%%
chrissentiment=[-1,1,1,1,1,1,1,-1,-1,0,1,1,-1,0,0,1,1,0,0,1,1,1,1,1,1,0,1,1,0,1,1,0,0,1,-1,1,1,1,-1,0,1,1,1,1,1,1,1,1,0,1]
#                                       ,great turnout         ,dont miss            ,dr fictner       ##for human error indexing purposes...
#chrissentiment=[1,1,-1,1,1,0,-1,-1,1,0,1,1,1,1,-1,1,1,1,1,1]  Was 75% with 20 samples.  Decided to go to 50samples for better confidence in results.
len(chrissentiment)


#%%
congressrand.insert(1,'Human_Sentiment',chrissentiment)


#%%
total=len(chrissentiment)
correct=0
for x in range(0,len(chrissentiment)):
    if congressrand.iloc[x]['Human_Sentiment']==congressrand.iloc[x]['Trinary_Score']:
        correct+=1
    
correct/total

#%% [markdown]
# Got 70% correct.    Over large sets it should be good enough.
# 

#%%
###This just shows what my predictions were and the classified scores on the test set I picked.
congressrand[['Trinary_Score','Human_Sentiment']]



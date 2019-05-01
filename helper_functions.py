#%% [markdown]
# All of the helper commands for filtering datasets to send just what you want to a visualization tool.
# 
# Designed so you send a dataset through a series of helper function filters, then send the final filtered dataset to a function that provides an answer
# 
# 20-April-2019
# 
# 21-April: Updated function names to be more intuitive/conventional

#%%


#%% [markdown]
# List of Helpers:
# 
# Filters
# 
# filter_age      Gives a dataset only including tweets by people above or below (or exactly) an age
# 
# filter_sentiment_type   Gives a dataset with only positive, negative, or neutral tweets
# 
# filter_sentiment_number Gives a dataset with sentiment valusea abve or below a number (find more extreme sentiment)
# 
# filter_gender   Gives a dataset with only tweets from specified gender
# 
# filter_leaning_tweets  Gives a dataset only from liberal or conservative
# 
# filter_persons_tweets  Gives dataset with only one person's tweets
# 
# filter_race_type   Gives a dataset containing only the race entered
# 
# 
# Answers
# 
# get_sentiment_count   Returns the count of tweets containing that classification of sentiment (+ 0 -)
# 
# get_total_tweet_count  Returns number of rows in dataset
# 
# get_retweets_per_tweet  Returns sum of retweet_count divided by number of tweets
# 
# get_average_sentiment  Returns the average sentiment score in a dataset
# 
# get_leaning_score Returns the political leaning score of a person
# 
# get_sentiment_frequency  returns proportion of tweets that are a particular type of sentiment
# 
# get_top_retweeted  returns a ranked dictionary of the most retweeted by their retweets_per_tweet and their retweet rates
# 
# get_most_conservative  returns a dictionary of the most conservative by dw_score and their scores
# 
# get_most liberal  Same as above but for liberal
# 
# get_most_positive  returns ranked dictionary of names and average sentiment of most positive average sentiment
# 
# get_most_negative  same as above for negative
# 
# 

#%%
import csv
import pandas as pd
import numpy as np


#%%
# trump=pd.read_csv('trump_sentiment.csv')
# clinton=pd.read_csv('clinton_sentiment.csv')
# congress=pd.read_csv('congress_sentiment.csv')
# all_names=congress['elite'].unique()


#%%



#%%



#%%
#congress.head()


#%%
##Valid arguments for side are "more than", "less than", "exactly"
def filter_age(dataset, age, side): 
    dataset['age']=pd.to_numeric(dataset['age'])
    if(side=="more than"):
        new_data=dataset['age']>age
    elif(side=="less than"):
        new_data=dataset['age']<age
    elif(side=="exactly"):
        new_data=dataset['age']==age
    else:
        print("age direction not given, ignoring age filter")
        return dataset   
    
    return dataset[new_data]


#%%
# x=filter_age(congress,64, side="d")
# x.head()


#%%
###direction takes "above", "below", "exactly"
def filter_sentiment_number(dataset, number, direction):
    if (number>1 or number<-1):
        print("\n"+"invalid number range, retruning entire dataset")
        return dataset
    
    if (direction=="above"):
        new_data=dataset['Vader_Score']>number
    elif(direction=="below"):
        new_data=dataset['Vader_Score']<number
    elif(direction=="exactly"):
        new_data=dataset['Vader_Score']==number
    else:
        print ("invalid direction given, returning entire dataset")
        return dataset
    
    
    return dataset[new_data]


#%%
#filter_sentiment_number(congress, 10, 'below')

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
##pnn takes "positive,", "negative", "neutral".  
def filter_sentiment_type(dataset, pnn):
    if (pnn=='positive'):
        new_data=dataset['Trinary_Score']==1
    elif (pnn=='negative'):
        new_data=dataset['Trinary_Score']==-1
    elif (pnn=='neutral'):
        new_data=dataset['Trinary_Score']==0
    else:
        print("invalid type given, returning entire dataset")
        return dataset
    
    return dataset[new_data]
    


#%%
##pnn takes "positive,", "negative", "neutral".  
def get_sentiment_count(dataset, pnn):
    num=get_sentiment_type(dataset,pnn).shape[0]
    return num


#%%
##Gender takes "male or "female"
def filter_gender(dataset, gender):
    if(gender==male):
        new_data=dataset['gender']==0.5
    elif(gender=="female"):
        new_data=dataset['gender']==-0.5
    else:
        print("invalid gender given, returning entire dataset")
        return dataset
    
    return dataset[new_data]


#%%
##leans takes liberal or conservative
def filter_leaning_tweets(dataset, leans):
    if(leans=="conservative"):
        new_data=dataset['dw_score']>0
    elif(leans=="liberal"):
        new_data=dataset['dw_score']<0
    else:
        print("invalid leaning given, returning entire dataset")
        return dataset
    
    return dataset[new_data]


#%%
def get_total_tweet_count(dataset):
    total, ignore =dataset.shape
    return total


#%%
def get_persons_tweet_count(dataset, name):
    pertinent=dataset['elite']==name
    return get_total_tweet_count(dataset[pertinent])


#%%



#%%
def filter_persons_tweets(dataset,name):
    pertinent=dataset['elite']==name
    return dataset[pertinent]


#%%
def get_total_retweet_count(dataset):
    the_sum=dataset['retweet_count'].sum()
    return the_sum


#%%



#%%
def get_retweets_per_tweet(dataset):
    rt=get_total_retweet_count(dataset)
    tw=get_total_tweet_count(dataset)
    ans=rt/tw
    return ans


#%%
def get_top_retweeted(dataset, num):
    rts=[]
    ranks={}
    final={}
    all_names=dataset['elite'].unique()
    for name in all_names:
        w=filter_persons_tweets(dataset,name)
        x=get_retweets_per_tweet(w)
        rts.append(x)
    for d,c in zip(all_names,rts):
        ranks.update({d:c})
    ranks_sorted=sorted(ranks, key=ranks.get, reverse=True)
    for name in ranks_sorted[0:num]:
        final.update({name:ranks[name]})
    return final
    


#%%
def get_average_sentiment(dataset):
    num=dataset.shape[0]
    sent=dataset['Vader_Score'].sum()
    return sent/num


#%%
#get_average_sentiment(filter_persons_tweets(congress, "_Hunter"))


#%%
#get_top_retweeted(congress,5)


#%%
def get_leaning_score(dataset,name):
    score=filter_persons_tweets(dataset,name)['dw_score'].max()
    return score


#%%



#%%
#get_leaning_score(congress,"_Hunter")


#%%
def get_most_conservative(dataset,num):
    rts=[]
    ranks={}
    final={}
    all_names=dataset['elite'].unique()
    for name in all_names:
        score=get_leaning_score(dataset,name)
        rts.append(score)
    for d,c in zip(all_names,rts):
        ranks.update({d:c})
    ranks_sorted=sorted(ranks, key=ranks.get, reverse=True)
    for name in ranks_sorted[0:num]:
        final.update({name:ranks[name]})
    return final


#%%
#get_most_conservative(congress,5)


#%%
def get_most_liberal(dataset,num):
    rts=[]
    ranks={}
    final={}
    all_names=dataset['elite'].unique()
    for name in all_names:
        score=get_leaning_score(dataset,name)
        rts.append(score)
    for d,c in zip(all_names,rts):
        ranks.update({d:c})
    ranks_sorted=sorted(ranks, key=ranks.get, reverse=False)
    for name in ranks_sorted[0:num]:
        final.update({name:ranks[name]})
    return final


#%%
#get_most_liberal(congress,6)


#%%
##Race is "white", or "not white"
def filter_race_type(dataset, race):
    if(race=="white"):
        new_data=dataset['race']==0.5
    elif(race=="not white"):
        new_data=dataset['race']==-0.5
    else:
        print("invalid race entered, returning entire dataset")
        return dataset
    return dataset[new_data]


#%%
##pnn takes "positive,", "negative", "neutral".  
def get_sentiment_frequency(dataset,pnn):
    count=filter_sentiment_type(dataset,pnn).shape[0]
    tot=dataset.shape[0]
    return count/tot
    


#%%
#get_sentiment_frequency(trump,'negative')


#%%
def get_most_positive(dataset,num):
    rts=[]
    ranks={}
    final={}
    all_names=dataset['elite'].unique()
    for name in all_names:
        dataset2=filter_persons_tweets(dataset,name)
        score=get_average_sentiment(dataset2)
        rts.append(score)
    for d,c in zip(all_names,rts):
        ranks.update({d:c})
    ranks_sorted=sorted(ranks, key=ranks.get, reverse=True)
    for name in ranks_sorted[0:num]:
        final.update({name:ranks[name]})
    return final


#%%
#get_most_positive(congress,10)


#%%
def get_most_negative(dataset,num):
    rts=[]
    ranks={}
    final={}
    all_names=dataset['elite'].unique()
    for name in all_names:
        dataset2=filter_persons_tweets(dataset,name)
        score=get_average_sentiment(dataset2)
        rts.append(score)
    for d,c in zip(all_names,rts):
        ranks.update({d:c})
    ranks_sorted=sorted(ranks, key=ranks.get, reverse=False)
    for name in ranks_sorted[0:num]:
        final.update({name:ranks[name]})
    return final


#%%



#%%



#%%



#%%



#%%



#%%



#%%



#%%



#%%



#%%



#%%




from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import numpy as np # I have found out that pandas sucks when working with large data sets apparently numpy is better when working with large data sets
# Assumption is that we might get comments 100k or more
import requests # for making http requests
import json # for parsing json data

def GetReviews(companyname,pageno):
    # convert company name where spaces are replaced with hyphens
    df = pd.DataFrame()
    companyname=companyname.replace(" ","-")
    url = 'https://api.hellopeter.com/consumer/business/'+companyname+'/reviews?page='+str(1)
    page = requests.get(url)
    jsondata=json.loads(page.text)    
    last_page=jsondata['last_page']        
    df = df.from_records(jsondata['data'])
    i = 1
    while i <= last_page:
        if pageno == 0:
            print("Processing page: "+str(i)+ " of "+str(last_page))
            pass
        else:
            print("Processing page: "+str(i)+ " of "+str(pageno))
            if i == pageno:
                break
        
        i = i + 1
        url = 'https://api.hellopeter.com/consumer/business/'+companyname+'/reviews?page='+str(i)
        page = requests.get(url)
        jsondata=json.loads(page.text)
        df = pd.concat([df,df.from_records(jsondata['data'])])
        
    return df

def FetchStats(slugname):
    url = 'https://api.hellopeter.com/consumer/business/'+slugname
    page = requests.get(url)
    jsondata=json.loads(page.text)
    return jsondata


#df = GetReviews("telkom",100)

def Analyze(df):
    sentiment = SentimentIntensityAnalyzer()
    # iterate over the data frame 
    for index, row in df.iterrows():
        currentReview = row['review_title']+'\n'+row['review_content']
        sentimentScore = sentiment.polarity_scores(currentReview)
        df.loc[index,'compound'] = sentimentScore['compound']
        df.loc[index,'neg'] = sentimentScore['neg']
        df.loc[index,'neu'] = sentimentScore['neu']
        df.loc[index,'pos'] = sentimentScore['pos']

    for index,row in df.iterrows():
        if row['compound'] >= 0.05:
            df.loc[index,'sentiment'] = 'positive'
        elif row['compound'] <= -0.05:
            df.loc[index,'sentiment'] = 'negative'
        else:
            df.loc[index,'sentiment'] = 'neutral'

    # count the number of positive, negative and neutral reviews
    print(df['sentiment'].value_counts())

    # print percentage of positive, negative and neutral reviews
    print(df['sentiment'].value_counts(normalize=True))

    # for each row in dataframe assign points
    for index,row in df.iterrows():
        # if positive and review_rating is 5 then assign 100 points and author_total_reviews_count > 5 
        if row['sentiment'] == 'positive' and row['review_rating'] == 5 and row['author_total_reviews_count'] >= 5:
            df.loc[index,'points'] = 100
        # if positive and review_rating is 5 then assign 80 points and author_total_reviews_count < 5
        elif row['sentiment'] == 'positive' and row['review_rating'] == 5 and row['author_total_reviews_count'] < 5:
            df.loc[index,'points'] = 80
        # if positive and review_rating is 4 then assign 60 points and author_total_reviews_count > 5
        elif row['sentiment'] == 'positive' and row['review_rating'] == 4 and row['author_total_reviews_count'] >= 5:
            df.loc[index,'points'] = 60
        # if positive and review_rating is 4 then assign 40 points and author_total_reviews_count < 5
        elif row['sentiment'] == 'positive' and row['review_rating'] == 4 and row['author_total_reviews_count'] < 5:
            df.loc[index,'points'] = 40
        # if positive and review_rating is 3 then assign 20 points and author_total_reviews_count > 5
        elif row['sentiment'] == 'positive' and row['review_rating'] == 3 and row['author_total_reviews_count'] >= 5:
            df.loc[index,'points'] = 20
        # if positive and review_rating is 3 then assign 10 points and author_total_reviews_count < 5
        elif row['sentiment'] == 'positive' and row['review_rating'] == 3 and row['author_total_reviews_count'] < 5:
            df.loc[index,'points'] = 10
        # if negative and review_rating is 1 then assign -100 points and author_total_reviews_count > 5
        elif row['sentiment'] == 'negative' and row['review_rating'] == 1 and row['author_total_reviews_count'] >= 5:
            df.loc[index,'points'] = -100
        # if negative and review_rating is 1 then assign -80 points and author_total_reviews_count < 5
        elif row['sentiment'] == 'negative' and row['review_rating'] == 1 and row['author_total_reviews_count'] < 5:
            df.loc[index,'points'] = -80
        # if negative and review_rating is 2 then assign -60 points and author_total_reviews_count > 5  
        elif row['sentiment'] == 'negative' and row['review_rating'] == 2 and row['author_total_reviews_count'] >= 5:
            df.loc[index,'points'] = -60
        # if negative and review_rating is 2 then assign -40 points and author_total_reviews_count < 5
        elif row['sentiment'] == 'negative' and row['review_rating'] == 2 and row['author_total_reviews_count'] < 5:
            df.loc[index,'points'] = -40
        # if negative and review_rating is 3 then assign -20 points and author_total_reviews_count > 5
        elif row['sentiment'] == 'negative' and row['review_rating'] == 3 and row['author_total_reviews_count'] >= 5:
            df.loc[index,'points'] = -20
        # if negative and review_rating is 3 then assign -10 points and author_total_reviews_count < 5
        elif row['sentiment'] == 'negative' and row['review_rating'] == 3 and row['author_total_reviews_count'] < 5:
            df.loc[index,'points'] = -10
        # if neutral and review_rating is 3 then assign 0 points and author_total_reviews_count > 5
        elif row['sentiment'] == 'neutral' and row['review_rating'] == 3 and row['author_total_reviews_count'] >= 5:
            df.loc[index,'points'] = 0
        # if neutral and review_rating is 3 then assign 0 points and author_total_reviews_count < 5
        elif row['sentiment'] == 'neutral' and row['review_rating'] == 3 and row['author_total_reviews_count'] < 5:
            df.loc[index,'points'] = 0
        # if neutral and review_rating is 4 then assign 0 points and author_total_reviews_count > 5
        elif row['sentiment'] == 'neutral' and row['review_rating'] == 4 and row['author_total_reviews_count'] >= 5:
            df.loc[index,'points'] = 0
        # if neutral and review_rating is 4 then assign 0 points and author_total_reviews_count < 5
        elif row['sentiment'] == 'neutral' and row['review_rating'] == 4 and row['author_total_reviews_count'] < 5:
            df.loc[index,'points'] = 0
        # if neutral and review_rating is 5 then assign 0 points and author_total_reviews_count > 5
        elif row['sentiment'] == 'neutral' and row['review_rating'] == 5 and row['author_total_reviews_count'] >= 5:
            df.loc[index,'points'] = 0
        # if neutral and review_rating is 5 then assign 0 points and author_total_reviews_count < 5
        elif row['sentiment'] == 'neutral' and row['review_rating'] == 5 and row['author_total_reviews_count'] < 5:
            df.loc[index,'points'] = 0

    # get maximum points
    maxpoints = len(df) * 100
    # score = total points / maximum points
    score = (df['points'].sum() / maxpoints) * 100    
    # work out average review rating
    avg_review_rating = df['review_rating'].mean()
    return df, score, avg_review_rating


    
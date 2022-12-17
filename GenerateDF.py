
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

def GetReviewsRating(companyname,pageno,rating):
    # convert company name where spaces are replaced with hyphens
    df = pd.DataFrame()
    companyname=companyname.replace(" ","-")
    url = 'https://api.hellopeter.com/consumer/business/'+companyname+'/reviews?page='+str(1)+'&ratings='+str(rating)
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
        url = 'https://api.hellopeter.com/consumer/business/'+companyname+'/reviews?page='+str(i)+'&ratings='+str(rating)
        page = requests.get(url)
        jsondata=json.loads(page.text)
        df = pd.concat([df,df.from_records(jsondata['data'])])        
    return df

def GenerateDf(companynames,pageno):
    df = pd.DataFrame()
    i = 0
    for companyname in companynames:
        i+=1
        print("Processing company: "+str(i)+ " of "+str(len(companynames)))        
        try:
            df = pd.concat([df,GetReviewsRating(companyname,pageno,1)])
        except:
            pass
        try:
            df = pd.concat([df,GetReviewsRating(companyname,pageno,2)])
        except:
            pass
        try:
            df = pd.concat([df,GetReviewsRating(companyname,pageno,3)])
        except:
            pass
        try:
            df = pd.concat([df,GetReviewsRating(companyname,pageno,4)])
        except:
            pass
        try:
            df = pd.concat([df,GetReviewsRating(companyname,pageno,5)])
        except:
            pass
        
        
    return df


df = GenerateDf(['telkom','airbnb','discovery-bank','outsurance','visa-logistics','ooba','active-glass-aluminium','elite-wall-and-roof-coating','ati-civils-pty-ltd','clear-view-frameless','diversit-e-smart-trade-college','dc-experts','the-garden-venue-boutique-hotel','prepaid24','wootware','msiza-it-shop','websitedesign-co-za','getsavvi-health','dr-melane-van-zyl-psychiatrist','solar-guru','drain-surgeon','international-employment-solutions','cartrack','securite','adt-security','flight-centre-travel-group','lift-airlines','distell','police-clear','tv-and-video-doctor','manna-health','miway','max-law-credit-legal','affinity-health','bonitas','trudon-publishers-of-the-yellow-pages','eezi-move','engen-petroleum','auction-na','road-protect-pty-ltd','parmalat','420monkeys','dinnertimestoriessa','betway','yesplaybet','sars','ethekwini','city-of-cape-town','transnet','hellopeter','sweepsouth','platinum-life','ombudsman','decor-essentials','simply-asia','mondo','mit-mak-motors','woodford-car-hire','isabella-garcia','hudsons-burger-joint','wisolar-wicorp-pty-ltd','1-grid','dunlop','perfect-laser-technologies-pty-limited','stss-prepaid-metering','o-yes-properties-1','the-mattress-warehouse','dhl-international'],100)

import os
try:
    os.mkdir("data")
except:
    pass
df.to_csv("data/rawdata.csv",index=False)

# generate column comment
df['comment'] = df['review_title'] + " " + df['review_content']

dfBad = df[df['review_rating'] < 3]
dfBad['sentiment'] = '0'

# for ratings 3 - 4 we will consider them as neutral
dfNeutral = df[df['review_rating'] == 3]  
dfNeutral4 = df[df['review_rating'] == 4]
dfNeutral = pd.concat([dfNeutral,dfNeutral4])
dfNeutral['sentiment'] = '2'
dfGood = df[df['review_rating'] == 5]
#for all dfGood sentiments are positive
dfGood['sentiment'] = '1'
# for dfBad only use columns comment,sentiment,review_rating,author_total_reviews_count
dfBad = dfBad[['comment','sentiment','review_rating','author_total_reviews_count']]
# for dfGood only use columns comment,sentiment,review_rating,author_total_reviews_count
dfGood = dfGood[['comment','sentiment','review_rating','author_total_reviews_count']]
dfNeutral = dfNeutral[['comment','sentiment','review_rating','author_total_reviews_count']]
# combine dfBad and dfGood
df = pd.concat([dfBad,dfGood,dfNeutral])
# save to csv
df.to_csv("data/trainingData.csv",index=False)




# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 17:15:50 2018

@author: bossaerts_bruno
"""
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

list_titles = []
list_number_comments = []
list_votes = []
list_tiers = []
list_post_dates = []


for i in range(1,10):     # Range should end at 103
    url = "https://www.kaggle.com/forums/167/topics.json?sortBy=new&group=all&page=" + str(i) + "&pageSize=20&category=all&kind=all"
    
    r = requests.get(url)                           # Go to website 
    soup = BeautifulSoup(r.text, "lxml")            # Make soup
    string = (soup.find_all('p')[0].get_text())     # Save paragraph as string
    
    print("Processing page: " + str(i))
    
    titles = re.findall(r'\"title\"\:"(.*?)\"', string)
    for title in titles:
        list_titles.append(title)

    number_comments = re.findall(r'\"commentCount\"\:(.*?)\,', string)
    for comment in number_comments:
        list_number_comments.append(comment)
    
    votes = re.findall(r'\"votes\"\:(.*?)\}', string)
    for vote in votes:
        list_votes.append(vote)
    
    tiers = re.findall(r'\"tier\"\:"(.*?)\"', string)
    for tier in tiers:
        list_tiers.append(tier)
    
    post_dates = re.findall(r'\"postDate\"\:"(.*?)"', string)
    for date in post_dates:
        list_post_dates.append(date)
        
    print("Lenght of lists: " + str(len(list_titles)))
    print(" ")



# PRINT PROGRESS
    
print(len(list_titles))
print(list_titles)
print(" ")

print(len(list_number_comments))
print(list_number_comments)
print(" ")

print(len(list_votes))
print(list_votes)
print(" ")

print(len(list_tiers))
print(list_tiers)
print(" ")

print(len(list_post_dates))
print(list_post_dates)
print(" ")

df = pd.DataFrame({'Title': list_titles,'Number comments': list_number_comments,'Votes': list_votes,'Tier': list_tiers,'Post date': list_post_dates})

# PROCESSING


df['Date'] = pd.to_datetime(df['Post date'])
df = df.drop('Post date', 1)

df['Weekday'] = df['Date'].apply(lambda x: x.weekday())

def convert_weekdays(x):
    if x == 0:
        return 'Monday'
    elif x == 1:
        return 'Tuesday'
    elif x == 2:
        return 'Wednesday'
    elif x == 3:
        return 'Thursday'
    elif x == 4:
        return 'Friday'
    elif x == 5:
        return 'Saturday'
    elif x == 6:
        return 'Sunday'

df['Weekday_name'] = df['Weekday'].apply(convert_weekdays)

# df = pd.DataFrame({'Title': list_titles,'Number comments': list_number_comments,'Votes': list_votes,'Tier': list_tiers,'Post date': list_post_dates})

# print(df)

# df.to_csv('output_raw.csv', index=False, header=True)

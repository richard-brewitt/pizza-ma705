# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 20:23:22 2020

@author: Richard Brewitt
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import re

    
#print(soup)

csv_file = open('data.csv', 'w', newline='')
writer = csv.writer(csv_file)

writer.writerow(['name', 'link', 'score', 'location', 'date'])


df = pd.DataFrame(columns=['name', 'link', 'score', 'location', 'date']) 
#pages = 31

for page in range(1,31):
    print("Getting Page:", page)
    soup = BeautifulSoup(requests.get("https://onebite.app/reviews/dave?page="+str(page)+"&minScore=0&maxScore=10").text, 'lxml')
    
  


    for review in soup.find_all('div', class_='jsx-596798944 col col--review'):
        data = []
        print("Getting Review Information")
        # Restaurant Name
        name = review.h2.text
        data.append(name)
        
        # Link Review Page
        link = "https://onebite.app{0}".format(review.a['href'])
        data.append(link)
        
       
        # Score
        score = review.p.text
        data.append(score)
        
        # Location
        location = review.find(class_='jsx-574827726 reviewCard__location').text
        data.append(location)
        
        # Date
        date = review.find(class_='jsx-2368882028 userMeta__timestamp').text
        data.append(date)
        
        #soup2 = BeautifulSoup(requests.get(link).text, 'lxml')
        #views = soup2.find('span', class_='jsx-1676893135 reviewViews').text
        #data.append(views)
             
        # make a row for this review
        #row = [name, score, location, link]
        # turn it into a series
        row = pd.Series(data, index=df.columns)
        df = df.append(row, ignore_index = True)
        
        # add to csv
        writer.writerow(row)
    
csv_file.close()

# change score to float
df['score'] = df['score'].astype(float) 

# get the state
df['state'] = df.location.str.slice(start=-2)

# get the city
df['city'] = df.location.str.slice(stop=-4)

# Get the time and adjust dates in terms of "days ago"
current_time = datetime.now()
for i in range(len(df)):
    if (len(df.date[i]) ==10) or (len(df.date[i]) ==14) or (len(df.date[i]) ==13) or (len(df.date[i])==9):
        days_ago = int(df.date[i][0])
        new_date = current_time - timedelta(days_ago)
        df['date'] = df['date'].replace(df.date[i],new_date)
# covert to datetime object
df.date = pd.to_datetime(df.date)


# Top 10 Scores
top_10_scores = df.nlargest(10, 'score')
#fig1 = top_10_scores.plot.scatter(x='score', y='name', title='Top 10 Scores')

# Histogram
#fig2 = plt.hist(df.score)

# Highest average scoring states
top5_states = df.groupby(['state']).mean().sort_values('score', ascending=False).head(5)

# Highest average scoring cities
top5_cities = df.groupby(['city']).mean().sort_values('score', ascending=False).head(5)

# Average Score
average_score = df['score'].mean()

# Reviews by state
state_counts = df.state.value_counts()
#fig_state_count = df['state'].value_counts().plot(kind='bar')
# plt.xlabel('States with Reviews')
# plt.ylable('Number of Reviews')
# plt.title('Number of Reviews by State')

# most reviewed cities
most_reviewed_cities = df.city.value_counts().head()
# most_reviewed_cities.plot(kind='barh')


########## SCRAPE SECOND PAGE #################

# make lists for scraped values to be added to df
address = []
maps_links = []
view_list = []
likes_list = []
compare_link = []

# Loop through df 
for i in range(len(df)):
    soup2 = BeautifulSoup(requests.get(df.link[i]).text, 'lxml')
    
    print('getting data on second page: ',i)
    
    # Get location data
    address_info = soup2.find('div', class_='jsx-84601126 location')
    full_address = address_info.text
    map_link = address_info.a['href']
    address.append(full_address)
    maps_links.append(map_link)   
    
    # Phone Number
    #phone = soup2.find('div', class_='jsx-127705284 phoneNumber')
    #phone = soup2.find('a', attrs={'class':'jsx-127705284'})
    #phone = phone.text
    #data2.append(phone)
    #df['phone'] = phone
    
    
    # Views
    views = soup2.find('span', attrs={'class':'jsx-1676893135'})
    views = views.text
    views = views[:-6]
    views = views.replace(',','')
    views = int(views)    
    view_list.append(views)

    
    # Likes
    likes = soup2.find('span', attrs={'class': 'jsx-1676893135 reviewLikes'})
    likes = likes.text
    likes = likes[:-6]
    likes = likes.replace(',','')
    likes = int(likes)   
    likes_list.append(likes)
    
    # Compare Link
    
    link_name = soup2.find('div', class_="jsx-84601126 name")
    cLink = link_name.a['href']
    cLink = 'https://onebite.app'+cLink
    compare_link.append(cLink)   



# add the lists to the df
df['address'] = address
df['map links'] = maps_links
df['views'] = view_list
df['likes'] = likes_list
df['cLink'] = compare_link

#################### Visualize Second Page Data###################
"""
# Top 10 Views
top_10_views = df.nlargest(10, 'views')
fig3 = top_10_views.plot.scatter(x='views', y='name', title='Top 10 Views')

# Likes Views & Scores Scatter Plot
df.plot.scatter(x='views', y='likes', c='score', s='score_sq', alpha=.5, colormap= 'rainbow',title='Likes Views & Scores')
plt.xlabel('Views')
plt.ylabel('Likes')
"""


### Comparison Page##########

score_overview = []

# Loop through df 

for i in range(len(df)):
    soup3 = BeautifulSoup(requests.get(df.cLink[i]).text, 'lxml')
    print("getting score comp data on: ", i)
       
    if soup3.find('div', class_="jsx-1258670469 ratingOverview") is not None:
        overview = soup3.find('div', class_="jsx-1258670469 ratingOverview").text
    else:
        overview = None
    score_overview.append(overview)



cust_Score = []
num_Revs = []
for i in range(len(score_overview)):
    print("getting scores and number of reviews on: ", i)    
    if score_overview[i] is not None:
        cScore = str([x for x in re.findall('[0-9]+\.[0-9]+', score_overview[i])][0])
        #cScore.astype(float)
        cust_Score.append(cScore)
        nR = str([y for y in re.findall('[0-9]+', score_overview[i])][-1])
        #nR = nR.astype(float)
        num_Revs.append(nR)
    else:
        cScore = None
        cust_Score.append(cScore)
        nR = None
        num_Revs.append(nR)        
    
df['cust_Score'] = cust_Score
df['cust_Score'] = df['cust_Score'].astype(float)
df['num_Revs'] = num_Revs
df['num_Revs'] = df['num_Revs'].astype(float)

df.to_csv('pizza.csv', encoding='utf-8', index=False)


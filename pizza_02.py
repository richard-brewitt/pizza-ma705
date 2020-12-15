# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 21:33:54 2020

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
from matplotlib.ticker import FuncFormatter
import plotly.express as px

df = pd.read_csv('pizza.csv')

########### fig1 -- Top 10 Scores ###########

top_10_scores = df.nlargest(10, 'score')
"""
fig1 = top_10_scores.plot.scatter(x=['score'], y='name', title='Top 10 Scores')
fig1.set_ylabel("Resturant Name")
fig1.set_xlabel("Dave's Score")
"""


# Histogram
#fig2 = plt.hist(df.score)

########## Highest average scoring states ############
top5_states = df.groupby(['state']).mean().sort_values('score', ascending=False).head(5)

state_avgs = df.groupby(['state']).mean()

# Highest average scoring cities
top5_cities = df.groupby(['city', 'state']).mean().sort_values('score', ascending=False).head(5)
top_cities = df.groupby(['city', 'state'] ).mean().sort_values('score', ascending=False)
######### Average Scores #############
dave_avg_score = df['score'].mean()
avg_cScore = df['cust_Score'].mean()


# Reviews by state
state_counts = df.state.value_counts() 
fig_state_count = df['state'].value_counts().plot(kind='bar')
# plt.xlabel('States with Reviews')
# plt.ylable('Number of Reviews')
# plt.title('Number of Reviews by State')


# most reviewed cities
most_reviewed_cities = df.city.value_counts().head()
# most_reviewed_cities.plot(kind='barh')



# Add the checklist -------------------------------------------------
    # html.Div([
    #         dcc.Checklist(
    #             id='my_checklist',                      # used to identify component in callback
    #             options=[
    #                      {'label': x, 'value': x, 'disabled':False}
    #                      for x in df['state'].unique()
    #             ],
    #             value=['NY','MA','PA'],    # values chosen by default

    #             className='my_box_container',           # class of the container (div)
    #             style={'display':'flex'},             # style of the container (div)

    #             inputClassName='my_box_input',          # class of the <input> checkbox element
    #             inputStyle={'cursor':'pointer'},      # style of the <input> checkbox element

    #             labelClassName='my_box_label',          # class of the <label> that wraps the checkbox input and the option's label
    #             labelStyle={'background':'red',   # style of the <label> that wraps the checkbox input and the option's label
    #                          'padding':'0.4rem 1rem',
    #                          'border-radius':'0.4rem'},

    #             #persistence='',                        # stores user's changes to dropdown in memory ( I go over this in detail in Dropdown video: https://youtu.be/UYH_dNSX1DM )
    #             #persistence_type='',                   # stores user's changes to dropdown in memory ( I go over this in detail in Dropdown video: https://youtu.be/UYH_dNSX1DM )
    #         ),
       
    #     ]),
    
    

#------------------------------------------------------------------------------
# Create Barchart for Average Review by State
# @app.callback(
#     Output(component_id='state_avg_graph', component_property='figure'),
#     [Input(component_id='my_checklist', component_property='value')]
# )
# def update_graph(options_chosen):

#     dff = df[df['state'].isin(options_chosen)]
#     print (dff['state'].unique())

#     barchart=px.bar(
#             data_frame=dff,
#             x='name',
#             y=['score', 'cust_Score'],
            
#             )

#     return (barchart)


# -------------------------------------------------------------------------------------













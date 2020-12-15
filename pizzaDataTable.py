# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 08:43:58 2020

@author: Richard Brewitt
"""

import dash  
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objects as go


# -------------------------------------------------------------------------------------
# Import the cleaned data (importing csv into pandas)
df = pd.read_csv('pizza.csv')
df = df.drop_duplicates(subset='name', keep="first")


# Creating an ID column name gives us more interactive capabilities
df['id'] = df['name']
df.set_index('id', inplace=True, drop=False)
print(df.columns)



fig3Dstate = px.scatter_3d(
    data_frame=df,
    x='cust_Score',
    y='score',
    z='num_Revs',
    color="state",
    #color_discrete_sequence=['magenta', 'green', 'red', 'blue', 'yellow'],
    #color_discrete_map={'NY': 'red', 'MA': 'blue', 'PA': 'magenta', 'NJ': 'green', 'FL': 'yellow'},
    opacity=0.4,              # opacity values range from 0 to 1
    symbol='state',            # symbol used for bubble
    #symbol_map={"NY": "circle", "MA": 'circle', "PA": 'circle', "NJ": 'circle', "FL": 'circle'}
    
    
    # size='resized_pop',       # size of bubble
    # size_max=50,              # set the maximum mark size when using size
    #log_x=True,  # you can also set log_y and log_z as a log scale
    # range_z=[9,13],           # you can also set range of range_y and range_x
    template='ggplot2',         # 'ggplot2', 'seaborn', 'simple_white', 'plotly',
                                # 'plotly_white', 'plotly_dark', 'presentation',
                                # 'xgridoff', 'ygridoff', 'gridon', 'none'
    title="The Best Pizza By State",
    #labels={'Years in school (avg)': 'Years Women are in School'},
    # hover_data={'Continent': False, 'GDP per capita': ':.1f'},
    hover_name='name',        # values appear in bold in the hover tooltip
    height=600,                 # height of graph in pixels
    
    #animation_frame='date',   # assign marks to animation frames
    range_x=[0.1,10],
    #range_z=[0,1600],
    range_y=[10,0.1]
)
# Use for animation rotation of 3d figures
x_eye = -1.25
y_eye = 2
z_eye = 0.5

fig3Dstate.update_layout(scene_camera_eye=dict(x=x_eye, y=y_eye, z=z_eye),
                  updatemenus=[dict(type='buttons',
                                    showactive=False,
                                    y=1,
                                    x=0.8,
                                    xanchor='left',
                                    yanchor='bottom',
                                    pad=dict(t=45, r=10),
                                    buttons=[dict(label='Play',
                                                  method='animate',
                                                  args=[None, dict(frame=dict(duration=500, redraw=True),
                                                                    transition=dict(duration=0),
                                                                    fromcurrent=True,
                                                                    mode='immediate'
                                                                    )]
                                                  )
                                              ]
                                    )
                                ]
                  )




dff2 = df[df['state'].isin(['NY', 'PA', 'MA'])]
fig3Dcity = px.scatter_3d(
    data_frame=dff2,
    x='cust_Score',
    y='score',
    z='num_Revs',
    color= dff2.state,
    opacity=0.7,              # opacity values range from 0 to 1
    symbol='state',            # symbol used for bubble
             # set the maximum mark size when using size
    #log_x=True,  # you can also set log_y and log_z as a log scale
    # range_z=[9,13],           # you can also set range of range_y and range_x
    color_discrete_map={'NY': 'blue', 'MA': 'red', 'PA': 'green'},
    template='ggplot2',         
    title="The Best Pizza in MA, NY, PA",
    #labels={'Years in school (avg)': 'Years Women are in School'},
    hover_name='name',        # values appear in bold in the hover tooltip
    height=600,                 # height of graph in pixels
    range_x=[0.1,10],
    #range_z=[0,1600],
    range_y=[10, .1]
)

fig3Dcity.update_layout(scene_camera_eye=dict(x=x_eye, y=y_eye, z=z_eye),
                  updatemenus=[dict(type='buttons',
                                    showactive=False,
                                    y=1,
                                    x=0.8,
                                    xanchor='left',
                                    yanchor='bottom',
                                    pad=dict(t=45, r=10),
                                    buttons=[dict(label='Play',
                                                  method='animate',
                                                  args=[None, dict(frame=dict(duration=500, redraw=True),
                                                                    transition=dict(duration=0),
                                                                    fromcurrent=True,
                                                                    mode='immediate'
                                                                    )]
                                                  )
                                              ]
                                    )
                                ]
                  )



def rotate_z(x, y, z, theta):
    w = x + 1j * y
    return np.real(np.exp(1j * theta) * w), np.imag(np.exp(1j * theta) * w), z


frames = []

for t in np.arange(0, 6.26, 0.1):
    xe, ye, ze = rotate_z(x_eye, y_eye, z_eye, -t)
    frames.append(go.Frame(layout=dict(scene_camera_eye=dict(x=xe, y=ye, z=ze))))
fig3Dstate.frames = frames
fig3Dcity.frames = frames


# -------------------------------------------------------------------------------------
# App layout
app = dash.Dash(__name__, prevent_initial_callbacks=True, external_stylesheets=[dbc.themes.SIMPLEX]) # this was introduced in Dash version 1.12.0
#
server = app.server
# Sorting operators (https://dash.plotly.com/datatable/filtering)
app.layout = html.Div([    # main div open
                       
    dbc.Row(dbc.Col(html.H1('Pizza Analytics'),
                        width={'size': 12, 'offset': 5},
                        ),
                ),

    html.H3('Richard Brewitt MA 705'),    
    html.Br(),
    html.P("""Data gathered for this project was scraped from Barstool's One Bite App.
           The app compiles Dave Portnoy's Pizza reviews wherein he rates each slice on
           a 0-10 scale. The app also allows users to place their own reviews and scores.
           The pizza review data within this dashboard is current as of November 30, 2020.
           """),
    
    html.A('Click here to visit the One Bite App', href='https://onebite.app/reviews/dave'),
    html.Br(),
    dcc.Markdown('''The table below can be filtered based on any column including
                  **state** and **city**, or by Dave's **score** or the average **cust_Score**
                  which is the average score a resturant receives from users who rate it on the app.
                  Doing so will cause the bar graph below to update with Dave's review score's 
                  following the selected criteria. 
                  This application of the data also fills a void
                  found on the One Bite App because their search engine is inadequate. On
                  the app, when somone searches *Boston*, locations such as *Boston's North End
                  Pizza* in Kanehoe Bay Drive, Kailua, Hawaii populate the results. This search
                  engine aggregates Dave's reviews by city and state so one can more 
                  easily and accurately view his highest rated scores by city and state.'''),
# DASH TABLE ---------------------------------------------------
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": True, "selectable": True, "hideable": True}
            if i == "iso_alpha3" or i == "year" or i == "id"
            else {"name": i, "id": i, "deletable": True, "selectable": True}
            for i in df.columns
        ],
        data=df.to_dict('records'),  # the contents of the table
        editable=True,              # allow editing of data inside all cells
        filter_action="native",     # allow filtering of data by user ('native') or not ('none')
        sort_action="native",       # enables data to be sorted per-column by user or not ('none')
        sort_mode="multi",         # sort across 'multi' or 'single' columns
        column_selectable="multi",  # allow users to select 'multi' or 'single' columns
        row_selectable="multi",     # allow users to select 'multi' or 'single' rows
        row_deletable=True,         # choose if user can delete a row (True) or not (False)
        selected_columns=[],        # ids of columns that user selects
        selected_rows=[],           # indices of rows that user selects
        page_action="native",       # all data is passed to the table up-front or not ('none')
        hidden_columns = ['id', 'cLink', 'map links'],
        page_current=0,             # page number that user is on
        page_size=5,                # number of rows visible per page
        style_cell={                # ensure adequate header width when text is shorter than cell's text
            'minWidth': 95, 'maxWidth': 95, 'width': 95
        },
        style_cell_conditional=[    # align text columns to left. By default they are aligned to right
            {
                'if': {'column_id': c},
                'textAlign': 'left'
            } for c in ['name', 'location', 'state','city', 'address', 'id']
        ],
        style_data_conditional=[
            {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
        }
    ],
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },
    
        style_data={                # overflow cells' content into multiple lines
            'whiteSpace': 'normal',
            'height': 'auto'
        }
    ),

    html.Br(),
    html.Br(),
    
# BAR CHART -------------------------------------------------------
    html.Div(id='bar-container'),
    
    html.Br(),
    html.Br(),
# ------------------------------------------------------------------

    dbc.Row(dbc.Col(html.H3("Use the range slider below to view Dave's average score and the average customer score by state on a map"),
                        width={'size': 12, 'offset': 0},
                        ),
                ),


    #html.H3("Use the range slider below to view Dave's Average Score by State on a map.", style='center'),


# SLIDER ------------------------------------------------  
    dcc.RangeSlider(
        id='my-range-slider',
        min=0,
        max=10,
        step=0.1,
        value=[5.0, 7.0],
        marks = {0:'0', 1:'1.0', 2:'2.0', 3:'3.0', 4:'4.0', 5:'5.0',
                 6:'6.0', 7:'7.0', 8:'8.0', 9:'9.0', 10:'10.0'},
        allowCross=False,
        dots = True,
        pushable = .5,
        updatemode='mouseup',
        #tooltip={'always_visible': True, 'placement':'top'}
    ),
    html.Div(id='output-container-range-slider'),
    
# CHOROPLETH MAP ----------------------------------------------    
    html.Div([
        dbc.Row([
            dbc.Col(dcc.Graph(id='choromap'),
                    width=6), # Dave's Avg by state
            dbc.Col(dcc.Graph(id='choromap2'),
                    width=6), # Cust Avg by state
            ])
 ]),
    html.Br(),
 # ------------------ 3D Div -----------------------                 
    dbc.Row(dbc.Col(html.H3("The following visualizations cross reference Dave's score with the average customer score and the number of reviews a restaurant has"
                            +" so that places with more reviews are higher on the plot and high scores are in the same corner"),
                    width={'size': 12, 'offset': 0},
                    ),
            ),

    html.Div([
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig3Dstate),
                   width=6),
            dbc.Col(dcc.Graph(figure=fig3Dcity),
                    width=6)
            ])

  ])

]) # main div close

                 

# -------------------------------------------------------------------------------------
# Create bar chart
@app.callback(
    Output(component_id='bar-container', component_property='children'),
    [Input(component_id='datatable-interactivity', component_property="derived_virtual_data"),
     Input(component_id='datatable-interactivity', component_property='derived_virtual_selected_rows'),
     Input(component_id='datatable-interactivity', component_property='derived_virtual_selected_row_ids'),
     Input(component_id='datatable-interactivity', component_property='selected_rows'),
     Input(component_id='datatable-interactivity', component_property='derived_virtual_indices'),
     Input(component_id='datatable-interactivity', component_property='derived_virtual_row_ids'),
     Input(component_id='datatable-interactivity', component_property='active_cell'),
     Input(component_id='datatable-interactivity', component_property='selected_cells')]
)
def update_bar(all_rows_data, slctd_row_indices, slct_rows_names, slctd_rows,
               order_of_rows_indices, order_of_rows_names, actv_cell, slctd_cell):
    print('***************************************************************************')
    print('Data across all pages pre or post filtering: {}'.format(all_rows_data))
    print('---------------------------------------------')
    print("Indices of selected rows if part of table after filtering:{}".format(slctd_row_indices))
    print("Names of selected rows if part of table after filtering: {}".format(slct_rows_names))
    print("Indices of selected rows regardless of filtering results: {}".format(slctd_rows))
    print('---------------------------------------------')
    print("Indices of all rows pre or post filtering: {}".format(order_of_rows_indices))
    print("Names of all rows pre or post filtering: {}".format(order_of_rows_names))
    print("---------------------------------------------")
    print("Complete data of active cell: {}".format(actv_cell))
    print("Complete data of all selected cells: {}".format(slctd_cell))

    dff = pd.DataFrame(all_rows_data)

    # used to highlight selected resturants on bar chart
    colors = ['red' if i in slctd_row_indices else '#0074D9'
              for i in range(len(dff))]

    if "name" in dff and "score" in dff:
        return [
            dcc.Graph(id='bar-chart',
                      figure=px.bar(
                          data_frame=dff,
                          x="name",
                          y='score',
                          #labels={"did online course": "% of Pop took online course"},
                          title="Dave's Pizza Review Scores"
                      ).update_layout(showlegend=False, xaxis={'categoryorder': 'total ascending'})
                      .update_traces(marker_color=colors, hovertemplate="<b>%{y}</b><extra></extra>")
                      )
        ]

# DONT CHANGE ABOVE
# -------------------------------------------------------------------------------------


# Create choropleth map of Dave's Avg Rev Score -----------------------------------------
@app.callback(
    Output(component_id='choromap', component_property='figure'),
    Input(component_id='my-range-slider', component_property='value')
    #[Input(component_id='datatable-interactivity', component_property="derived_virtual_data"),
     #Input(component_id='datatable-interactivity', component_property='derived_virtual_selected_rows')]
)
def update_map(sliders):
    print(sliders)
    print(type(sliders))
    
    state_avgs = df.groupby(['state']).mean().reset_index()
    state_avgs = state_avgs[(state_avgs['score'] > sliders[0])&(state_avgs['score']< sliders[1])]

    fig = px.choropleth(
            data_frame=state_avgs,
            locations= state_avgs['state'],
            locationmode="USA-states",
            scope="usa",
            color='score',
            color_continuous_scale="inferno",
            range_color=(0,10),
            labels={'score': "Dave's Avg Score", "cust_Score": "Avg Customer Score"},
            title="Dave's Average Score by State",
            template='ggplot2',
            hover_data=['state', 'score', 'cust_Score']
        )
    fig.update_layout(showlegend=False, title=dict(font=dict(size=28), x=0.5, xanchor='center'))
                                                               
    return fig
@app.callback(
    Output(component_id='choromap2', component_property='figure'),
    Input(component_id='my-range-slider', component_property='value')
)
def update_map2(sliders):
    print(sliders)
    print(type(sliders))
    
    state_avgs2 = df.groupby(['state']).mean().reset_index()
    state_avgs2 = state_avgs2[(state_avgs2['cust_Score'] > sliders[0])&(state_avgs2['cust_Score']< sliders[1])]

    fig2 = px.choropleth(
            data_frame=state_avgs2,
            locations= state_avgs2['state'],
            locationmode="USA-states",
            scope="usa",
            color='cust_Score',
            color_continuous_scale="inferno",
            range_color=(0,10),
            labels={'cust_Score': "Avg Customer Score", "score":"Dave's Avg Score"},
            title="Customers Average Score by State",
            template='ggplot2',
            hover_data=['state', 'cust_Score', 'score']
        )
    fig2.update_layout(showlegend=False, title=dict(font=dict(size=28), x=0.5, xanchor='center'))
                                                               
    return fig2
# -------------------------------------------------------------------------------------


# Highlight selected column -------------------------------------
@app.callback(
    Output('datatable-interactivity', 'style_data_conditional'),
    [Input('datatable-interactivity', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': {'column_id': i},
        'background_color': '#D2F3FF'
    } for i in selected_columns]





# DONT CHANGE BELOW -------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True, port=8055)
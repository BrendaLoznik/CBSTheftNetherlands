#!/usr/bin/env python
# coding: utf-8

# In[1]:


#1.1 LOAD LIBRARIES
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import geojson
import mapbox
import streamlit as st


# In[23]:


#1.2 LOAD DATA I
data = pd.read_csv('data.csv')


# In[24]:


#1.2 LOAD DATA II
data_pivot = pd.read_csv('data_pivot.csv',  dtype={'id': 'str'})


# In[25]:


#1.2 LOAD DATA III
#geojson
municipality_json = geojson.load(open('geojson_gemeente_2020.geojson', 'r'))

#create id in geojson
for feature in municipality_json['features']:
    feature['id'] = feature['properties']['code']


# In[27]:


#2 STREAMLIT SETTINGS

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Thefts in The Netherlands",
    page_icon=':cop:',
    layout="wide",  # centered
    initial_sidebar_state="auto")  # collapsed

#CREATE COLUMNS
t1, t2 = st.columns((0.1,1)) #0.07,1
t1.image('cbs_icon.png', width = 120)
t2.title("Statistics Netherlands - Reported Thefts")


# In[28]:


#CREATE SIDEBAR
st.sidebar.title("Menu")

#THEFT SELECT BOX
thefts = data['theft'].unique()       
theft = st.sidebar.selectbox('Type of theft', (thefts))

#MUNICIPALITY SELEX TBOX
municipalities = data['municipality'].unique().tolist()
default_ix = municipalities.index('Amsterdam')
municipality = st.sidebar.selectbox('Select a municipality', municipalities, index=default_ix)

#YEAR SELECT BOX
year= st.sidebar.radio(label ='Year', options = ['2018', '2019', '2020', '2021'], index =2)
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

#TOP X SLIDER
top =  st.sidebar.slider('How many types of theft do you want to see?', 1, 10, 5)

# ADD REFERENCES TO CODE AND DATA
st.sidebar.title("References")
st.sidebar.write(
        """Data: [CBS Statline 2022](https://opendata.cbs.nl/statline/#/CBS/nl/dataset/83651NED/table?fromstatweb)
        """)
st.sidebar.write(
        """Source code: [Github](https://github.com/BrendaLoznik/CBSTheftNetherlands/blob/master/app.py)
        """)


# In[ ]:





# In[ ]:


#3.1 COMMON TYPES OF THEFT IN THE NETHERLANDS

#CREATE COLUMNS
col1, col2, col3 = st.columns(3)

with col1:
    st.write(' ')

with col2:
    st.subheader('Top ' + str(top) + ' most common thefts by year')

with col3:
    st.write(' ')
    
#CREATE COLUMNS
col4, col5 = st.columns([3, 0.1])

#CREATE DF
common_crime = data.groupby(['year', 'theft'])['count'].sum().reset_index()
common_crime['rank'] = common_crime.groupby(by=['year'])['count'].transform(lambda x: x.rank(ascending=False))
common_crime['year'] = common_crime['year'].astype('str')
common_crime = common_crime.sort_values(['year', 'rank'])
top_rank = np.arange(1, top+1 , 1).tolist()
common_crime= common_crime[(common_crime['rank'].isin(top_rank))]

#CREATE PLOT
fig2 = px.bar(data_frame = common_crime, 
             x = 'year',
             y = 'count',
             height = 600,
            #  text_auto=True,
             #text_auto='.2s',
             color = 'theft',
         #   color_discrete_map = {'bike': 'rgb(0,0,128)', 'shoplifting': 'rgb(235,207,52)'},
             color_discrete_sequence = px.colors.qualitative.Prism,
             hover_name = 'theft',
            hover_data = {'theft': False, 'year': False, 'count': True}
            )

#update layout
fig2.update_layout({ #'title': {'text': 'Top ' + str(top) + ' most common thefts in The Netherlands by year', 'x': 0.5},
                     'legend': {'title': 'Type of theft'},
                  })

#st.plotly_chart(fig2)
col4.plotly_chart(fig2, use_container_width=True) 


# In[ ]:


#3.2 WHERE DO THEFTS OCCURE

#CREATE COLUMNS
col6, col7 = st.columns(2)

with col6:
    st.subheader('Registered '+ theft + ' in '+ str(year))
    
with col7:
    st.subheader('Top 10 manunicpalities with the higest rate of '+ theft + ' in ' + year) 

#CREATE DF
data_graph = data_pivot.copy()
data_graph ['year'] = data_graph ['year'].astype('str')
data_graph = data_graph  [data_graph ['year']==year]
data_graph = data_graph[['id', 'province', 'municipality', 'year', theft]]
data_graph  ['log scale'] = np.log10(data_graph [theft]+1)

#CREATE PLOT
fig1 = px.choropleth_mapbox(data_frame = data_graph,
              locations= "id",
              geojson = municipality_json,
              mapbox_style = 'carto-positron',
              center = {'lat': 52.153, 'lon':5.3842 },
             zoom = 6.5,
             height=800 ,
             width=800, 
             #COLOR
             color = 'log scale',
             opacity  = 0.4,
             color_continuous_scale="Purples",
            range_color=(0, data_graph['log scale'].max()),
            #HOVER INFO
            hover_name = 'municipality',
            hover_data = {'id': False, 'log scale': False, theft: True}
           )


#update layout
fig1.update_layout({ #'title': {'text': 'Registered '+ theft + ' in The Netherlands in '+ str(year), 'x': 0.5},
                     'legend': {'title': 'log scale'},
                  })


#st.plotly_chart(fig1)
col6.plotly_chart(fig1, use_container_width=True) 


# ## 2.3 Greatest risk

# In[ ]:


#3.3 TOP 10 MUNICIPALITIES

#CREATE DF
worst_crime = data.groupby(['year',  'municipality', 'theft'])['count'].sum().reset_index()
worst_crime = worst_crime.sort_values(['year', 'theft', 'count'], ascending=[True,False, False]) 
worst_crime ['rank'] = worst_crime .groupby(by=['year', 'theft'])['count'].transform(lambda x: x.rank(ascending=False))
worst_crime = worst_crime[['year', 'theft', 'rank', 'count', 'municipality']]
worst_crime ['year'] = worst_crime ['year'].astype('str')
worst_crime = worst_crime[(worst_crime['theft']== theft)  & (worst_crime['year']== year)]
worst_crime  = worst_crime[0:10]
worst_crime   = worst_crime.sort_values('rank', ascending = False)

#CREATE PLOT
fig5 = px.bar(data_frame = worst_crime ,
             y = 'municipality',
             x = 'count',
             height = 800,
              text_auto=True,
            # text_auto='.2s',
             orientation = 'h',
             color_discrete_sequence  = ['rgb(95, 70,144)'],
            hover_data = {'municipality': False,  'count': False}
            )

#update layout
fig5.update_layout({ #'title': {'text': 'Top 10 municipalities with the highest rate of ' + theft + ' in ' + str(year) , 'x': 0.5},
                   'yaxis': {'title': {'text' : ''}} ,
                  })


#st.plotly_chart(fig5)
col7.plotly_chart(fig5, use_container_width=True) 


# ## 2.4 Crime in your municipality

# In[ ]:


#3.4 CRIME IN YOUR MUNICIPALITY

#SET CUSTOM LABELS
if theft =='street robbery':
    label = 'Street robbery'
elif theft == 'shoplifting':
    label = 'Shoplifting'
elif theft == 'pickpocketing':
    label = 'Pickpocketing'
elif theft == 'motorcycle/scooter theft':
    label = 'Motorcycle/scooter theft'
elif theft == 'moped theft':
    label = 'Moped theft'
elif theft == 'heist':
    label = 'Heist'
elif theft == 'car theft':
    label = 'Car theft'
elif theft == 'boat theft':
    label = 'Boat theft'
elif theft == 'bike theft':
    label = 'Bike theft'
elif theft == 'animal theft':
    label = 'Animal theft'
else:
    label = 'other'
    
#CREATE COLUMNS
col8, col9 = st.columns(2)

with col8:
    st.subheader('Most common theft crimes in ' + municipality + ' in ' + str(year) )
    
with col9:
    st.subheader( label + ' trend in ' +  municipality )
    
#CREATE DF
municipality_crime = data.groupby(['year',  'municipality', 'theft'])['count'].sum().reset_index()
municipality_crime ['rank'] = municipality_crime .groupby(by=['municipality', 'year'])['count'].transform(lambda x: x.rank(ascending=False))
municipality_crime ['year'] = municipality_crime ['year'].astype('str')
municipality_crime = municipality_crime[(municipality_crime['year']==year) & (municipality_crime['municipality']==municipality)]
municipality_crime = municipality_crime .sort_values('rank')

#CREATE PLOT
fig3 = px.bar(data_frame = municipality_crime,
             x = 'theft',
             y = 'count',
             height = 600,
              text_auto=True,
            # text_auto='.2s',
            # color_discrete_sequence = px.colors.qualitative.Prism,
              color_discrete_sequence  = ['rgb(29, 105, 150)'],
            hover_data = {'theft': False,  'count': False}
            )

#update layout
fig3.update_layout({ #'title': {'text': 'Most common theft crimes in ' + municipality + ' in ' + str(year)  , 'x': 0.5},
                   'xaxis': {'title': {'text' : ''}} ,
                  })

#st.plotly_chart(fig3)
col8.plotly_chart(fig3, use_container_width=True) 


# In[46]:


#3.5 tHEFT TREND

#CREATE DATASET
municipality_trend = data.groupby(['year',  'municipality', 'theft'])['count'].sum().reset_index()
municipality_trend  =municipality_trend .sort_values(['municipality', 'theft', 'year','count'], ascending=[True,True, True, True]) 
municipality_trend ['year'] = municipality_trend['year'].astype('str')
municipality_trend = municipality_trend[(municipality_trend ['municipality']== municipality) & (municipality_trend ['theft']== theft)  ]

#CREATE PLOT
fig4 = px.line(data_frame = municipality_trend,
             x= 'year',
             y = 'count',
            height = 600,
             color_discrete_sequence  = ['rgb(56, 166, 165)'],
            hover_data = {'year': False,  'count': True}
             )


   #update layout
fig4.update_layout({ #'title': {'text':  label + ' trend in ' +  municipality , 'x': 0.5},
                  })

#st.plotly_chart(fig4)
col9.plotly_chart(fig4, use_container_width=True) 


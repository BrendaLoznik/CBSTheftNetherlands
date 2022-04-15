#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 1 Housekeeping


# In[2]:


## 1.1 Load libraries


# In[3]:


import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import geojson
import mapbox
import streamlit as st


# In[4]:


## 1.2 Load data


# In[9]:


#load cleaned dataset
data = pd.read_csv(r'D:\Jupyter Notebooks\cbs-diefstal\data\data.csv')
data.head()


# In[10]:


#load cleaned dataset
data = pd.read_csv(r'D:\Jupyter Notebooks\cbs-diefstal\data\data.csv')
data.head()


# In[14]:


#load pivoted dataset
data_pivot = pd.read_csv(r'D:\Jupyter Notebooks\cbs-diefstal\data\data_pivot.csv',  dtype={'id': 'str'})
data_pivot.head()


# In[11]:


#geojson
municipality_json = geojson.load(open('geojson_gemeente_2020.geojson', 'r'))

#create id in geojson
for feature in municipality_json['features']:
    feature['id'] = feature['properties']['code']


# In[12]:


# 2 Streamlit settings


# In[17]:


# page conf
st.set_page_config(
    page_title="Theft crimes in The Netherlands",
    page_icon="🐍",
    layout="centered",  # wide
    initial_sidebar_state="auto")  # collapsed


# In[18]:


#create theft selectbox
theft = st.sidebar.selectbox('Type of theft', ('bike theft', 'moped theft', 'motorcycle/scooter theft',
      'car theft', 'boat theft', 'animal theft', 'street robbery',
      'pickpocketing', 'shoplifting', 'heist'))

#st.write('You selected:',theft)


# In[19]:


#create theft selectbox
municipality = st.sidebar.selectbox('Municipality', ('Aa en Hunze', 'Aalburg', 'Aalsmeer', 'Aalten', 'Achtkarspelen',
       'Alblasserdam', 'Albrandswaard', 'Alkmaar', 'Almelo', 'Almere',
       'Alphen aan den Rijn', 'Alphen-Chaam', 'Altena', 'Ameland',
       'Amersfoort', 'Amstelveen', 'Amsterdam', 'Apeldoorn', 'Appingedam',
       'Arnhem', 'Assen', 'Asten', 'Baarle-Nassau', 'Baarn',
       'Barendrecht', 'Barneveld', 'Bedum', 'Beek', 'Beekdaelen',
       'Beemster', 'Beesel', 'Berg en Dal', 'Bergeijk', 'Bergen (L.)',
       'Bergen (NH.)', 'Bergen op Zoom', 'Berkelland', 'Bernheze', 'Best',
       'Beuningen', 'Beverwijk', 'De Bilt', 'Binnenmaas', 'Bladel',
       'Blaricum', 'Bloemendaal', 'Bodegraven-Reeuwijk', 'Boekel',
       'Ten Boer', 'Borger-Odoorn', 'Borne', 'Borsele', 'Boxmeer',
       'Boxtel', 'Breda', 'Brielle', 'Bronckhorst', 'Brummen', 'Brunssum',
       'Bunnik', 'Bunschoten', 'Buren', 'Capelle aan den IJssel',
       'Castricum', 'Coevorden', 'Cranendonck', 'Cromstrijen', 'Cuijk',
       'Culemborg', 'Dalfsen', 'Dantumadiel', 'Delft', 'Delfzijl',
       'Deurne', 'Deventer', 'Diemen', 'Dinkelland', 'Doesburg',
       'Doetinchem', 'Dongen', 'Dongeradeel', 'Dordrecht', 'Drechterland',
       'Drimmelen', 'Dronten', 'Druten', 'Duiven', 'Echt-Susteren',
       'Edam-Volendam', 'Ede', 'Eemnes', 'Eemsdelta', 'Eemsmond',
       'Eersel', 'Eijsden-Margraten', 'Eindhoven', 'Elburg', 'Emmen',
       'Enkhuizen', 'Enschede', 'Epe', 'Ermelo', 'Etten-Leur',
       'Ferwerderadiel', 'De Fryske Marren', 'Geertruidenberg',
       'Geldermalsen', 'Geldrop-Mierlo', 'Gemert-Bakel', 'Gennep',
       'Giessenlanden', 'Gilze en Rijen', 'Goeree-Overflakkee', 'Goes',
       'Goirle', 'Gooise Meren', 'Gorinchem', 'Gouda', 'Grave',
       "'s-Gravenhage", 'Groningen', 'Grootegast', 'Gulpen-Wittem',
       'Haaksbergen', 'Haaren', 'Haarlem',
       'Haarlemmerliede en Spaarnwoude', 'Haarlemmermeer', 'Halderberge',
       'Hardenberg', 'Harderwijk', 'Hardinxveld-Giessendam', 'Haren',
       'Harlingen', 'Hattem', 'Heemskerk', 'Heemstede', 'Heerde',
       'Heerenveen', 'Heerhugowaard', 'Heerlen', 'Heeze-Leende', 'Heiloo',
       'Den Helder', 'Hellendoorn', 'Hellevoetsluis', 'Helmond',
       'Hendrik-Ido-Ambacht', 'Hengelo', "'s-Hertogenbosch", 'Heumen',
       'Heusden', 'Hillegom', 'Hilvarenbeek', 'Hilversum',
       'Hoeksche Waard', 'Hof van Twente', 'Het Hogeland',
       'Hollands Kroon', 'Hoogeveen', 'Hoorn', 'Horst aan de Maas',
       'Houten', 'Huizen', 'Hulst', 'IJsselstein', 'Kaag en Braassem',
       'Kampen', 'Kapelle', 'Katwijk', 'Kerkrade', 'Koggenland',
       'Kollumerland en Nieuwkruisland', 'Korendijk',
       'Krimpen aan den IJssel', 'Krimpenerwaard', 'Laarbeek', 'Landerd',
       'Landgraaf', 'Landsmeer', 'Langedijk', 'Lansingerland', 'Laren',
       'Leek', 'Leerdam', 'Leeuwarden', 'Leiden', 'Leiderdorp',
       'Leidschendam-Voorburg', 'Lelystad', 'Leudal', 'Leusden',
       'Lingewaal', 'Lingewaard', 'Lisse', 'Lochem', 'Loon op Zand',
       'Lopik', 'Loppersum', 'Losser', 'Maasdriel', 'Maasgouw',
       'Maassluis', 'Maastricht', 'De Marne', 'Marum', 'Medemblik',
       'Meerssen', 'Meierijstad', 'Meppel', 'Middelburg',
       'Midden-Delfland', 'Midden-Drenthe', 'Midden-Groningen',
       'Mill en Sint Hubert', 'Moerdijk', 'Molenlanden', 'Molenwaard',
       'Montferland', 'Montfoort', 'Mook en Middelaar', 'Neder-Betuwe',
       'Nederweert', 'Neerijnen', 'Nieuwegein', 'Nieuwkoop', 'Nijkerk',
       'Nijmegen', 'Nissewaard', 'Noardeast-Fryslân', 'Noord-Beveland',
       'Noordenveld', 'Noordoostpolder', 'Noordwijk', 'Noordwijkerhout',
       'Nuenen, Gerwen en Nederwetten', 'Nunspeet', 'Nuth', 'Oegstgeest',
       'Oirschot', 'Oisterwijk', 'Oldambt', 'Oldebroek', 'Oldenzaal',
       'Olst-Wijhe', 'Ommen', 'Onderbanken', 'Oost Gelre', 'Oosterhout',
       'Ooststellingwerf', 'Oostzaan', 'Opmeer', 'Opsterland', 'Oss',
       'Oud-Beijerland', 'Oude IJsselstreek', 'Ouder-Amstel', 'Oudewater',
       'Overbetuwe', 'Papendrecht', 'Peel en Maas', 'Pekela',
       'Pijnacker-Nootdorp', 'Purmerend', 'Putten', 'Raalte',
       'Reimerswaal', 'Renkum', 'Renswoude', 'Reusel-De Mierden',
       'Rheden', 'Rhenen', 'Ridderkerk', 'Rijssen-Holten', 'Rijswijk',
       'Roerdalen', 'Roermond', 'De Ronde Venen', 'Roosendaal',
       'Rotterdam', 'Rozendaal', 'Rucphen', 'Schagen', 'Scherpenzeel',
       'Schiedam', 'Schiermonnikoog', 'Schinnen', 'Schouwen-Duiveland',
       'Simpelveld', 'Sint Anthonis', 'Sint-Michielsgestel',
       'Sittard-Geleen', 'Sliedrecht', 'Sluis', 'Smallingerland', 'Soest',
       'Someren', 'Son en Breugel', 'Stadskanaal', 'Staphorst',
       'Stede Broec', 'Steenbergen', 'Steenwijkerland', 'Stein',
       'Stichtse Vecht', 'Strijen', 'Súdwest-Fryslân', 'Terneuzen',
       'Terschelling', 'Texel', 'Teylingen', 'Tholen', 'Tiel', 'Tilburg',
       'Tubbergen', 'Twenterand', 'Tynaarlo', 'Tytsjerksteradiel', 'Uden',
       'Uitgeest', 'Uithoorn', 'Urk', 'Utrecht', 'Utrechtse Heuvelrug',
       'Vaals', 'Valkenburg aan de Geul', 'Valkenswaard', 'Veendam',
       'Veenendaal', 'Veere', 'Veldhoven', 'Velsen', 'Venlo', 'Venray',
       'Vianen', 'Vijfheerenlanden', 'Vlaardingen', 'Vlieland',
       'Vlissingen', 'Voerendaal', 'Voorschoten', 'Voorst', 'Vught',
       'Waadhoeke', 'Waalre', 'Waalwijk', 'Waddinxveen', 'Wageningen',
       'Wassenaar', 'Waterland', 'Weert', 'Weesp', 'Werkendam',
       'West Betuwe', 'West Maas en Waal', 'Westerkwartier', 'Westerveld',
       'Westervoort', 'Westerwolde', 'Westland', 'Weststellingwerf',
       'Westvoorne', 'Wierden', 'Wijchen', 'Wijdemeren',
       'Wijk bij Duurstede', 'Winsum', 'Winterswijk', 'Woensdrecht',
       'Woerden', 'De Wolden', 'Wormerland', 'Woudenberg', 'Woudrichem',
       'Zaanstad', 'Zaltbommel', 'Zandvoort', 'Zederik', 'Zeewolde',
       'Zeist', 'Zevenaar', 'Zoetermeer', 'Zoeterwoude', 'Zuidhorn',
       'Zuidplas', 'Zundert', 'Zutphen', 'Zwartewaterland', 'Zwijndrecht',
       'Zwolle'))

#st.write('You selected:',municipality)


# In[20]:


#create theft selectbox
year= st.sidebar.selectbox('Year', ('2018', '2019', '2020', '2021'))

#st.write('You selected:',year)


# In[21]:


# Create top x slider

#st.subheader('Slider')
top =  st.sidebar.slider('How many types of theft do you want to see?', 1, 10, 5)
#st.write("You selected top ", top ,' thefts')


# In[ ]:





# ## 2.2 Where do the thefts occure?

# In[27]:


#create a custom df
data_graph = data_pivot.copy()
data_graph ['year'] = data_graph ['year'].astype('str')
data_graph = data_graph  [data_graph ['year']==year]
data_graph = data_graph[['id', 'province', 'municipality', 'year', theft]]
data_graph  ['log scale'] = np.log10(data_graph [theft]+1)


# In[ ]:


st.markdown( **'hello'**)


# In[29]:


#create map
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
fig1.update_layout({ 'title': {'text': 'Registered '+ theft + ' in The Netherlands in '+ str(year), 'x': 0.5},
                     'legend': {'title': 'log scale'},
                  })


st.plotly_chart(fig1)


# In[ ]:


## 2.3 What is the most common type of theft?


# In[32]:


common_crime = data.groupby(['year', 'theft'])['count'].sum().reset_index()
common_crime['rank'] = common_crime.groupby(by=['year'])['count'].transform(lambda x: x.rank(ascending=False))
common_crime['year'] = common_crime['year'].astype('str')
common_crime = common_crime.sort_values(['year', 'rank'])

#select top rank
#top = int(top)
top_rank = np.arange(1, top+1 , 1).tolist()
common_crime= common_crime[(common_crime['rank'].isin(top_rank))]


# In[31]:


#create bar plot
fig2 = px.bar(data_frame = common_crime, 
             x = 'year',
             y = 'count',
             height = 500,
            #  text_auto=True,
             #text_auto='.2s',
             color = 'theft',
         #   color_discrete_map = {'bike': 'rgb(0,0,128)', 'shoplifting': 'rgb(235,207,52)'},
             color_discrete_sequence = px.colors.qualitative.Prism,
             hover_name = 'theft',
            hover_data = {'theft': False, 'year': False, 'count': True}
            )

#update layout
fig2.update_layout({ 'title': {'text': 'Top ' + str(top) + ' most common thefts in The Netherlands by year', 'x': 0.5},
                     'legend': {'title': 'Type of theft'},
                  })

st.plotly_chart(fig2)


# In[ ]:


## 2.4 Crime in your municipality


# In[33]:


#create df
municipality_crime = data.groupby(['year',  'municipality', 'theft'])['count'].sum().reset_index()
municipality_crime ['rank'] = municipality_crime .groupby(by=['municipality', 'year'])['count'].transform(lambda x: x.rank(ascending=False))
municipality_crime ['year'] = municipality_crime ['year'].astype('str')
municipality_crime = municipality_crime[(municipality_crime['year']==year) & (municipality_crime['municipality']==municipality)]
municipality_crime = municipality_crime .sort_values('rank')


# In[34]:


#create bar plot
fig3 = px.bar(data_frame = municipality_crime,
             x = 'theft',
             y = 'count',
             height = 500,
              text_auto=True,
            # text_auto='.2s',
             color_discrete_sequence = px.colors.qualitative.Prism,
            hover_data = {'theft': False,  'count': False}
            )

#update layout
fig3.update_layout({ 'title': {'text': 'Most common theft crimes in ' + municipality + ' in ' + str(year)  , 'x': 0.5},
                   'xaxis': {'title': {'text' : ''}} ,
                  })

st.plotly_chart(fig3)


# In[ ]:


## 2.4 Municipality theft trends


# In[35]:


#create dataset
municipality_trend = data.groupby(['year',  'municipality', 'theft'])['count'].sum().reset_index()
municipality_trend  =municipality_trend .sort_values(['municipality', 'theft', 'year','count'], ascending=[True,True, True, True]) 
municipality_trend ['year'] = municipality_trend['year'].astype('str')
municipality_trend = municipality_trend[(municipality_trend ['municipality']== municipality) & (municipality_trend ['theft']== theft)  ]


# In[36]:


fig4 = px.line(data_frame = municipality_trend,
             x= 'year',
             y = 'count',
             color_discrete_sequence  = ['rgb(56, 166, 165)'],
            hover_data = {'year': False,  'count': True}
             )

#set custom label
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

   #update layout
fig4.update_layout({ 'title': {'text':  label + ' trend in ' +  municipality , 'x': 0.5},
                  })

st.plotly_chart(fig4)


# In[ ]:


## 2.5 Greatest risk


# In[37]:


worst_crime = data.groupby(['year',  'municipality', 'theft'])['count'].sum().reset_index()
worst_crime = worst_crime.sort_values(['year', 'theft', 'count'], ascending=[True,False, False]) 
worst_crime ['rank'] = worst_crime .groupby(by=['year', 'theft'])['count'].transform(lambda x: x.rank(ascending=False))
worst_crime = worst_crime[['year', 'theft', 'rank', 'count', 'municipality']]
worst_crime ['year'] = worst_crime ['year'].astype('str')
worst_crime = worst_crime[(worst_crime['theft']== theft)  & (worst_crime['year']== year)]
worst_crime  = worst_crime[0:10]
worst_crime   = worst_crime.sort_values('rank', ascending = False)


# In[39]:


#create bar plot
fig5 = px.bar(data_frame = worst_crime ,
             y = 'municipality',
             x = 'count',
             height = 500,
              text_auto=True,
            # text_auto='.2s',
             orientation = 'h',
             color_discrete_sequence  = ['rgb(29, 105, 150)'],
            hover_data = {'municipality': False,  'count': False}
            )

#update layout
fig5.update_layout({ 'title': {'text': 'Top 10 municipalities with the highest rate of ' + theft + ' in ' + str(year) , 'x': 0.5},
                   'yaxis': {'title': {'text' : ''}} ,
                  })


st.plotly_chart(fig5)


# In[ ]:





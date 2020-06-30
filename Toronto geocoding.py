#!/usr/bin/env python
# coding: utf-8

# In[9]:


get_ipython().run_line_magic('pip', 'install --user geocoder')


# In[2]:


import geocoder
import pandas as pd
import requests
from bs4 import BeautifulSoup


# In[3]:


wiki_url='https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'
resp = requests.get(wiki_url).text


# In[10]:


table = BeautifulSoup(resp, 'xml')#Beautiful Soup to Parse the url page


# In[11]:


column_names=['Postalcode','Borough','Neighbourhood']
df = pd.DataFrame(columns=column_names)


# In[12]:



# extracting information from the table
for tr_cell in table.find_all('tr'):
    row_data=[]
    for td_cell in tr_cell.find_all('td'):
        row_data.append(td_cell.text.strip())
    if len(row_data)==3:
        df.loc[len(df)] = row_data


# In[13]:


df.head()


# In[14]:


#remove rows where Borough is assigned
df = df[df['Borough']!= 'Not assigned']


# In[16]:


df.head()


# In[17]:


# group multiple Neighbourhood under one Postcode
temp_df=df.groupby('Postalcode')['Neighbourhood'].apply(lambda x: "%s" % ', '.join(x))
temp_df=temp_df.reset_index(drop=False)
temp_df.rename(columns={'Neighbourhood':'Neighbourhood_joined'},inplace=True)


# In[18]:


# join the newly constructed joined data frame
df_merge = pd.merge(df, temp_df, on='Postalcode')


# In[19]:


# drop the Neighbourhood column
df_merge.drop(['Neighbourhood'],axis=1,inplace=True)


# In[20]:


# drop duplicates from the data frame
df_merge.drop_duplicates(inplace=True)


# In[21]:


# rename Neighbourhood_joined back to Neighbourhood
df_merge.rename(columns={'Neighbourhood_joined':'Neighbourhood'},inplace=True)


# In[22]:


df_merge.head()


# In[23]:


df_merge.shape


# In[24]:


def get_geocode(postal_code):
    # initialize your variable to None
    lat_lng_coords = None
    while(lat_lng_coords is None):
        g = geocoder.google('{}, Toronto, Ontario'.format(postal_code))
        lat_lng_coords = g.latlng
    latitude = lat_lng_coords[0]
    longitude = lat_lng_coords[1]
    return latitude,longitude


# In[25]:


# takes a long time to get the data
#get_geocode('M3A')

# so we will use the csv sheet provided by Coursera as an alternative
geo_df=pd.read_csv('http://cocl.us/Geospatial_data')


# In[26]:


geo_df.head()


# In[27]:


geo_df.rename(columns={'Postal Code':'Postalcode'},inplace=True)
geo_merged = pd.merge(geo_df, df_merge, on='Postalcode')


# In[28]:


geo_merged.head()


# In[29]:


geo_merged.head()


# In[30]:


# correcting the sequence of data
geo_data=geo_merged[['Postalcode','Borough','Neighbourhood','Latitude','Longitude']]


# In[31]:


geo_data.head()


# In[ ]:





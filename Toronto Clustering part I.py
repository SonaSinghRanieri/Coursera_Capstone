#!/usr/bin/env python
# coding: utf-8

# ## Toronto explore and cluster neighbourhood

# In[93]:


import pandas as pd
import requests
from bs4 import BeautifulSoup


# In[94]:


wiki_url='https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'
resp = requests.get(wiki_url).text


# In[95]:


soup = BeautifulSoup(resp, 'xml')#Beautiful Soup to Parse the url page


# In[96]:


table=soup.find('table')


# In[97]:


column_names=['Postalcode','Borough','Neighbourhood']
df = pd.DataFrame(columns=column_names)


# In[98]:


# extracting information from the table
for tr_cell in table.find_all('tr'):
    row_data=[]
    for td_cell in tr_cell.find_all('td'):
        row_data.append(td_cell.text.strip())
    if len(row_data)==3:
        df.loc[len(df)] = row_data


# In[99]:


df.head()


# In[100]:


# remove rows where Borough is 'Not assigned'
df=df[df['Borough']!='Not assigned']


# In[101]:


df.head()


# In[102]:


# group multiple Neighbourhood under one Postcode
temp_df=df.groupby('Postalcode')['Neighbourhood'].apply(lambda x: "%s" % ', '.join(x))
temp_df=temp_df.reset_index(drop=False)
temp_df.rename(columns={'Neighbourhood':'Neighbourhood_joined'},inplace=True)


# In[103]:


# join the newly constructed joined data frame
df_merge = pd.merge(df, temp_df, on='Postalcode')


# In[104]:


# drop the Neighbourhood column
df_merge.drop(['Neighbourhood'],axis=1,inplace=True)


# In[105]:


# drop duplicates from the data frame
df_merge.drop_duplicates(inplace=True)


# In[106]:


# rename Neighbourhood_joined back to Neighbourhood
df_merge.rename(columns={'Neighbourhood_joined':'Neighbourhood'},inplace=True)


# In[107]:


df_merge.head()


# In[108]:


df_merge.shape


# In[ ]:





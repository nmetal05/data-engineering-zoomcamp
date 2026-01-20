#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


data_source = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
df = pd.read_csv(data_source + 'yellow_tripdata_2021-01.csv.gz', nrows=100)


# In[3]:


df


# In[4]:


df.head()


# In[5]:


df.dtypes


# In[6]:


df.shape


# In[7]:


dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

df = pd.read_csv(
    data_source + 'yellow_tripdata_2021-01.csv.gz',
    nrows=100,
    dtype=dtype,
    parse_dates=parse_dates
)


# In[8]:


df


# In[9]:


df.dtypes


# In[34]:


from sqlalchemy import create_engine
from tqdm.auto import tqdm


# In[14]:


engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')


# In[16]:


engine.connect()


# In[18]:


print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))


# In[35]:


df.head(n=0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')


# In[36]:


df_iter = pd.read_csv(
    data_source + 'yellow_tripdata_2021-01.csv.gz',
    nrows=100,
    dtype=dtype,
    parse_dates=parse_dates,
    iterator=True,
    chunksize=100000
)


# In[37]:


first = True

for df_chunk in tqdm(df_iter):

    if first:
        df_chunk.head(0).to_sql(
            name="yellow_taxi_data",
            con=engine,
            if_exists="replace"
        )
        first = False
        print("Table created")

    # Insert chunk
    df_chunk.to_sql(
        name="yellow_taxi_data",
        con=engine,
        if_exists="append"
    )

    print("Inserted:", len(df_chunk))


# In[ ]:





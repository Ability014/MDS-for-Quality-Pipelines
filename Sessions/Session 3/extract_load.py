""" 
    This code intend to load data from S3 bucket into your postgres db. You can modify the code in to suit the purpose you need it for.
    For this exercise, you will need to load the adventures work data instead.
    Note that you will need to some details to be completed where you have ... within this code
""" 

# pip install pandas
# pip install sqlalchemy
# pip install psycopg2 
# pip install boto3
# Install the packages above in your virtual environment if you don't have them. For pyscopg2, you can install its corresponding binary instead
# To perform the installation, remove the comment symbol from the pip install above
import boto3
import pandas as pd
from sqlalchemy import create_engine
import os
import re

s3 = boto3.resource(
    service_name='s3',
    region_name='eu-north-1',
    aws_access_key_id='enter the access key id',
    aws_secret_access_key='enter the secret access key'
)

# Assign your bucket object to my_bucket
my_bucket = s3.Bucket('jaffle-shop-mds')

# Print all associated objects of the bucket
for bucket in s3.buckets.all():
    for key in bucket.objects.all():
        print(key.key)

""" 
    Assign each bucket object to a variable, an example has been provided for you below 
    (all bucket objects have been provided for you in the notes.md)
"""
aw_address = s3.Bucket('jaffle-shop-mds').Object('adventure-works/address.csv').get()
aw_countryregion = s3.Bucket('jaffle-shop-mds').Object('adventure-works/countryregion.csv').get()
aw_creditcard = s3.Bucket('jaffle-shop-mds').Object('adventure-works/creditcard.csv').get()
...

# put each object into a list as below
df_list = [aw_address, aw_countryregion, aw_creditcard, ...]

""" 
    Before the step below, login to your postgres server and create a new database called: adventure_works, 
    and a new schema called: raw within adventure_works
"""
# create connection to your postgres db, remember to edit the dbname part to adventure_works as you have created from above
engine = create_engine("postgresql+psycopg2://postgres:password1234@localhost:5433/<dbname>")

""" 
    Put the names of what you want the data to be named in the postgres db, let the naming correspond with your bucket object name 
    in the order you have created the df_list. An example has been created for you. 
"""
df_names = ['raw_address', 'raw_countryregion', 'raw_creditcard', ...]
i = 0
for df in df_list:
    df_table = pd.read_csv(df['Body'])
    print(f'Loading table {df_names[i]}')
    df_table.to_sql(df_names[i], \
        engine, \
        schema = 'raw', \
        if_exists = 'replace', \
        index = False)
    print(f'Loaded table {df_names[i]}')
    i += 1

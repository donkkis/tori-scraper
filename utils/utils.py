import os
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv('.env-dev')

URI = os.getenv("MONGODB_URI_DEV")
DB_NAME = "tavaralle-hinta-dev"
CLIENT = MongoClient(URI)
DB = CLIENT[DB_NAME]

def dump_dev_db():
    """Will potentially fetch a large number of records. Use caution."""
    try:
        global DB
        listings = DB['listings']
        data = [{'Title': l['title'], 'Description': l['description']} for l in list(listings.find())]
        data = pd.DataFrame(data)
        data.to_csv('./data/descriptions.csv')
        return True
    except(Exception):
        print('Unknown exception, data has not been written')
        return False
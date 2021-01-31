import os
import pymongo
import json

from datetime import datetime as dt
from dotenv import load_dotenv
load_dotenv('.env-dev')

TIMEF = '%Y-%m-%d %H:%M:%S'
TIMEF_2 = '%Y-%m-%d %H:%M:%S.%f'

client = pymongo.MongoClient(os.getenv('MONGODB_URI_DEV'))
db = client['tavaralle-hinta-dev']

listings = db['listings']
listings.drop()
with open('./data/listings.json', 'r') as f:
    items = json.load(f)
items = list(map(lambda d: {**d, 'time_stamp': dt.strptime(d['time_stamp'], TIMEF)}, items))
items = [{k: v for k, v in d.items() if k != '_id'} for d in items]
listings.insert_many(items)

insertOps = db['insertOps']
insertOps.drop()
with open('./data/insertOps.json', 'r') as f:
    ops = json.load(f)
ops = list(map(lambda d: {**d, 'created': dt.strptime(d['created'], TIMEF_2)}, ops))
ops = [{k: v for k, v in d.items() if k != '_id'} for d in ops]
insertOps.insert_many(ops)

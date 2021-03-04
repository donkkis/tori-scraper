import os
import argparse
from dotenv import load_dotenv
from pymongo import MongoClient
from nlp.nlp import get_tags


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', default='../data/tags.csv')
    parser.add_argument('--target', default='file')

    args = parser.parse_args()
    tags = get_tags()

    if args.target == 'file':
        tags.to_csv(args.path)
    
    elif args.target == 'dev':
        load_dotenv('../.env-dev')
        uri = os.getenv('MONGODB_URI_DEV')
        db_name = 'tavaralle-hinta'
        client = MongoClient(uri)
        db = client[db_name]
        db.tags.insert_many(tags.to_dict(orient='records'))

    elif args.target == 'prod':
        load_dotenv('../.env')
        uri = os.getenv('MONGODB_URI')
        db_name = 'tavaralle-hinta'
        client = MongoClient(uri)
        db = client[db_name]
        db.tags.insert_many(tags.to_dict(orient='records'))

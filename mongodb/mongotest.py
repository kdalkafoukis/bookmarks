#!/usr/bin/env python3.7

# http://api.mongodb.com/python/current/tutorial.html
# test the mongodb DB with pymongo library 

from scripts.config import config

from pymongo import MongoClient

try:
    client = MongoClient(config['mongodb_url'], config['mongodb_port'])
    db = client.bookmarks
    print(db)
except:
    pass
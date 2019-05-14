#!/usr/bin/env python3.7

# http://api.mongodb.com/python/current/tutorial.html
# test the mongodb DB with pymongo library 

from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client.test_database

print(db)
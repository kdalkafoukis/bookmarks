from mongodbscripts import findDocuments
from config import config

key = 'docker'
db_name = config['bookmarks_db']
collection_name = config['bookmarks_collection']
findDocuments(key,db_name,collection_name)
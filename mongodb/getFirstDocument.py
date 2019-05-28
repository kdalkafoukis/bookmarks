from scripts.config import config
from mongodb.mongodbscripts import findDocuments

def getFirstDocument():
    key = 'docker'
    db_name = config['bookmarks_db']
    collection_name = config['bookmarks_collection']
    findDocuments(key,db_name,collection_name,1)
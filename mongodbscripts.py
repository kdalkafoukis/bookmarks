from pymongo import MongoClient
from datetime import datetime

def insertDocument(document,db_name,collection_name):
    client = MongoClient()
    db = client[db_name]
    collection = db[collection_name]
    collection.insert_one(document)

# hello world example find documents that refer to quantum keyword

def findDocument():
    client = MongoClient()
    db = client.boookmarks
    bookmarks = db.boookmarks

    collection = bookmarks.find()

    # keysToMatch = ("quantum")
    key = "quantum"

    exec_start = datetime.now()
    for bookmark in collection:
        # if all (bookmark['text'] and key in bookmark['text'].keys() for key in keysToMatch):  # filter keys
        if (bookmark['text']):
            if key in bookmark['text'].keys():
                pass
                # print(bookmark['name'])
                # print(bookmark['url'])
    exec_end = datetime.now()

    time = exec_end - exec_start
    print(time)
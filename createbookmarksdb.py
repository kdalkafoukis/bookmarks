from pymongo import MongoClient

def insertDocument(bookmark):
    client = MongoClient()
    db = client.boookmarks
    boookmarks = db.boookmarks
    boookmarks.insert_one(bookmark)

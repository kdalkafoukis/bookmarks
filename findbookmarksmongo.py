from pymongo import MongoClient
import pprint

client = MongoClient()
db = client.boookmarks
bookmarks = db.boookmarks
collection = bookmarks.find_one()
pprint.pprint(collection['name'])
pprint.pprint(collection['url'])

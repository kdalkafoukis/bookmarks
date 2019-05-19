# this script gets the saved bookmarks and saves the text
# from every url to the database
from datetime import datetime

from transformbookmarks import transformBookmarks
from mongodbscripts import insertDocument

from config import config

def testInsertOne(bookmarks):
    url = bookmarks[0]['url']
    text = transformBookmarks(url)
    first_bookmark = bookmarks[0]
    if (text):
        database_name = config['bookmarks_test_db']
        collection_name = config['bookmarks_test_collection']

        first_bookmark["text"] = text
        first_bookmark["created"] = datetime.utcnow()
        first_bookmark["modified"] = first_bookmark["created"]
       
        insertDocument(first_bookmark,database_name,collection_name)
        print(first_bookmark)

def insertAll(bookmarks):
    for bookmark in bookmarks:
        url = bookmark['url']
        text = transformBookmarks(url)
        if (text):
                database_name = config['bookmarks_db']
                collection_name = config['bookmarks_collection']

                bookmark["text"] = text
                bookmark["created"] = datetime.utcnow()
                bookmark["modified"] = bookmark["created"]

                insertDocument(bookmark,database_name,collection_name)
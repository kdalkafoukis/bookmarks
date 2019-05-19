from sys import argv
from createbookmarksdb import insertAll, testInsertOne
from getbookmarks import getBookmarks
from config import config

bookmarks = getBookmarks(config['browser'])

for arg in argv[:]:
    if (arg == "-ia"):
        insertAll(bookmarks)
    else:
        testInsertOne(bookmarks)


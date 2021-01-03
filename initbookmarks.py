from scripts.config import config

from sys import argv

from scripts.createbookmarksdb import insertAll, testInsertOne
from scripts.getbookmarks import getBookmarks

bookmarks = getBookmarks(config['browser'])

if (len(argv) <= 1):
    testInsertOne(bookmarks)
elif (argv[1] == "-ia"):
    insertAll(bookmarks)


from scripts.config import config

from sys import argv

from scripts.createbookmarksdb import insertAll, testInsertOne
from scripts.getbookmarks import getBookmarks

bookmarks = getBookmarks(config['browser'])

for arg in argv[1:]:
    if (arg == "-ia"):
        insertAll(bookmarks)
    else:
        testInsertOne(bookmarks)


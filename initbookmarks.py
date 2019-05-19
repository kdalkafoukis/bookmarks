from sys import argv
from createbookmarksdb import insertAll, testInsertOne
from getbookmarks import getBookmarks

bookmarks = getBookmarks("chrome")

for arg in argv[:]:
    if (arg == "-ia"):
        insertAll(bookmarks)
    else:
        testInsertOne(bookmarks)


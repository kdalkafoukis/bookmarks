from sys import argv
from createbookmarksdb import insertAll, testInsertOne
for arg in argv[:]:
    if (arg == "-ia"):
        insertAll()
else:
    testInsertOne()


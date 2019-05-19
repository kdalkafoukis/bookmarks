from mongodbscripts import findDocuments, copyCollections

key = 'quantum'
db_name = 'bookmarks'
collection_name = 'bookmarks'
findDocuments(key,db_name,collection_name)
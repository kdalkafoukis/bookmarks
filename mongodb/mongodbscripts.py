from pymongo import MongoClient
from datetime import datetime
from scripts.config import config

def insertDocument(document,db_name,collection_name):
    try:
        client = MongoClient(config['mongodb_url'], config['mongodb_port'])
        db = client[db_name]
        collection = db[collection_name]
        collection.insert_one(document)
    except:
        pass

def findDocuments(key,db_name,collection_name,numberOfDocuments):
    try:
        client = MongoClient(config['mongodb_url'], config['mongodb_port'])
        db = client[db_name]

        collection = db[collection_name]

        documents = collection.find()

        exec_start = datetime.now()
        
        arrayOfFirst_numberOfDocuments_Documents = documentsToArrayOf_numberOfDocuments_Documents(documents,key,numberOfDocuments)
        exec_end = datetime.now()

        time = exec_end - exec_start
        
        printDocuments(arrayOfFirst_numberOfDocuments_Documents,time,key)

        return arrayOfFirst_numberOfDocuments_Documents
    except:
        return {}

def copyCollections(db_old_name,db_new_name,collection_old_name,collection_new_name):
    try:
        client = MongoClient()
        old_db = client[db_old_name]
        new_db = client[db_new_name]

        old_collection = old_db[collection_old_name]
        new_collection = new_db[collection_new_name]

        old_collection_documents = old_collection.find()
        
        for old_document in old_collection_documents:
            new_collection.insert_one(old_document)
    except:
        pass
    
    return 0


def documentsToArrayOf_numberOfDocuments_Documents(documents,key,numberOfDocuments):
    arrayOfFirst_numberOfDocuments_Documents = []
    counter = 0
    for document in documents:
        # keysToMatch = ("quantum")
        # if all (bookmark['text'] and key in bookmark['text'].keys() for key in keysToMatch):  # filter keys
        if (document['text'] and document['name'] and document['url']):
            if key in document['text'].keys():
                if (counter < numberOfDocuments):
                    arrayOfFirst_numberOfDocuments_Documents.append({
                        'name': document['name'],
                        'url': document['url']
                    })

                counter = counter + 1
    return arrayOfFirst_numberOfDocuments_Documents


def printDocuments(arrayOfDocuments,time,key):
    counter = 0
    for document in arrayOfDocuments:
        print(counter,document)
        counter = counter + 1
    print('time: ',time,'\n','key: ',key,'\n')
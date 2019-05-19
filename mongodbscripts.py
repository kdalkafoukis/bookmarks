from pymongo import MongoClient
from datetime import datetime
from config import config

def insertDocument(document,db_name,collection_name):
    try:
        client = MongoClient(config['mongodb_url'], config['mongodb_port'])
        db = client[db_name]
        collection = db[collection_name]
        collection.insert_one(document)
    except:
        pass

def findDocuments(key,db_name,collection_name):
    try:
        client = MongoClient(config['mongodb_url'], config['mongodb_port'])
        db = client[db_name]

        collection = db[collection_name]

        results = collection.find()

        exec_start = datetime.now()
        
        condition = True
        first_res = {}

        for result in results:
            # keysToMatch = ("quantum")
            # if all (bookmark['text'] and key in bookmark['text'].keys() for key in keysToMatch):  # filter keys
            if (result['text']):
                if key in result['text'].keys():
                    if (condition):
                        first_res['name'] = result['name']
                        first_res['url'] = result['url']
                        condition = False

        exec_end = datetime.now()

        time = exec_end - exec_start
        
        print('time: ',time,'\n','key: ',key,'\n','first result: ',first_res)

        return results
    except:
        return {}

def copyCollections(db_old,db_new,collection_old,collection_new):
    try:
        client = MongoClient()
        old_db = client[db_old]
        new_db = client[db_new]

        old_collection = old_db[collection_old]
        new_collection = new_db[collection_new]

        results = old_collection.find()
        
        for result in results:
            new_collection.insert_one(result)
    except:
        pass
    
    return 0
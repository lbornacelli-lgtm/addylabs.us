import pymongo
import sys
sys.path.append('/home/ubuntu/addylabs')

MONGO_URI = "mongodb://addylabs:1002LBorn1!@10.0.0.1:27017/addylabs"
DB_NAME = "addylabs"

def get_db():
    client = pymongo.MongoClient(MONGO_URI)
    return client[DB_NAME]

def insert(collection, document):
    db = get_db()
    result = db[collection].insert_one(document)
    print(f"Inserted: {result.inserted_id}")
    return result.inserted_id

def find(collection, query={}):
    db = get_db()
    return list(db[collection].find(query))

def find_one(collection, query={}):
    db = get_db()
    return db[collection].find_one(query)

def update(collection, query, update):
    db = get_db()
    result = db[collection].update_one(query, {"$set": update})
    print(f"Modified: {result.modified_count}")
    return result.modified_count

def delete(collection, query):
    db = get_db()
    result = db[collection].delete_one(query)
    print(f"Deleted: {result.deleted_count}")
    return result.deleted_count

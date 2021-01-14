import random

from pymongo import MongoClient

client = MongoClient("mongodb://root:password@localhost:27017/?serverSelectionTimeoutMS=5000&connectTimeoutMS=10000&authSource=admin&authMechanism=SCRAM-SHA-256")
database = client["adminhub"]
collection = database["question"]

query = {}

cursor = collection.find({})
for q in cursor:
    collection.update_one({"_id": q['_id']}, {"$set": {"triggered_count": random.randint(1000, 5000)}})


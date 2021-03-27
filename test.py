import random

from bson import ObjectId
from pymongo import MongoClient

client = MongoClient(
    "mongodb://root:password@localhost:27017/?serverSelectionTimeoutMS=5000&connectTimeoutMS=10000&authSource=admin&authMechanism=SCRAM-SHA-256")
database = client["adminhub"]
question_collection = database["question"]
message_collection = database["message"]
flow_collection = database["flow"]

query = {}

# # add triggered count
# cursor = question_collection.find({})
# for q in cursor:
#     question_collection.update_one({"_id": q['_id']}, {"$set": {"triggered_count": random.randint(1000, 5000)}})
# # add triggered count(flow)
# cursor = flow_collection.find({})
# for q in cursor:
#     flow_collection.update_one({"_id": q['_id']}, {"$set": {"triggered_count": random.randint(300, 5000)}})
# add handler
message_collection.update_many({"receiver_id": ObjectId('5c78f794df78b45f7f8c6a5e')}, {"$set": {"handler": 'bot'}})
message_collection.update_many({"sender_id": ObjectId('5c78f794df78b45f7f8c6a5e')}, {"$set": {"handler": 'user'}})

import random

from pymongo import MongoClient

client = MongoClient(
    "mongodb://root:password@localhost:27017/?serverSelectionTimeoutMS=5000&connectTimeoutMS=10000&authSource=admin&authMechanism=SCRAM-SHA-256")
database = client["adminhub"]
question_collection = database["question"]
message_collection = database["message"]
flow_collection = database["flow"]

"""
add triggered count
"""
# cursor = question_collection.find({})
# for q in cursor:
#     question_collection.update_one({"_id": q['_id']}, {"$set": {"triggered_count": random.randint(1000, 5000)}})

"""
add triggered count(flow)
"""

# cursor = flow_collection.find({})
# for q in cursor:
#     flow_collection.update_one({"_id": q['_id']}, {"$set": {"triggered_count": random.randint(300, 5000)}})

"""
add handler
"""
# message_collection.update_many({"receiver_id": ObjectId('5c78f794df78b45f7f8c6a5e')}, {"$set": {"handler": 'bot'}})
# message_collection.update_many({"sender_id": ObjectId('5c78f794df78b45f7f8c6a5e')}, {"$set": {"handler": 'user'}})

"""
add nlp confidence
"""
# #11 min - 954180
# cursor = message_collection.update_many({}, {"$unset": {"chatbot.highest_confidence": ""}})
#
# query = {"handler": "bot",
#          "$or": [{"chatbot.qnid": {"$exists": True}},
#                  {"chatbot.unanswered": {"$exists": True}}]}
#
# cursor = message_collection.find(query)
# for q in cursor:
#     score = random.uniform(0.2, 0.8)
#     if matched_questions := q.get('nlp', {}).get('nlp_response', {}).get('matched_questions', {}):
#         score = matched_questions[0]['score']
#     message_collection.update_one({"_id": q['_id']}, {"$set": {"chatbot.highest_confidence": score}})

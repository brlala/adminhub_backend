from pymongo import MongoClient

client = MongoClient(
    "mongodb://root:password@localhost:27017/?serverSelectionTimeoutMS=5000&connectTimeoutMS=10000&authSource=admin&authMechanism=SCRAM-SHA-256")
database = client["adminhub"]
question_collection = database["question"]
message_collection = database["message"]

query = {}
#
# # add triggered count
# cursor = question_collection.find({})
# for q in cursor:
#     collection.update_one({"_id": q['_id']}, {"$set": {"triggered_count": random.randint(1000, 5000)}})
#
# # NOT USED
# cursor = message_collection.find({}, sort=[(u"_id", -1)])
# for q in cursor:
#     try:
#         if q['nlp']['nlp_response']['matched_questions'][0]['score']:
#             message_collection.update_one({"_id": q['_id']}, {
#                 "$set": {"chatbot.score": q['nlp']['nlp_response']['matched_questions'][0]['score'],
#                          "chatbot.topic": q['nlp']['nlp_response']['matched_questions'][0]['topic'],
#                          "chatbot.text": q['nlp']['nlp_response']['matched_questions'][0]['question_text'], }})
#     except:
#         pass

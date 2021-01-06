from motor.motor_asyncio import AsyncIOMotorClient

from app.env_variables import local_config

db = AsyncIOMotorClient(local_config.MONGODB_URL, maxPoolSize=100, minPoolSize=0)[local_config.DATABASE_NAME]
# class DataBase:
#     client: AsyncIOMotorClient = None
#
# db = DataBase()
#
# async def get_database() -> AsyncIOMotorDatabase:
#     return db.client[local_config.DATABASE_NAME]
#
#
# async def connect_to_mongo():
#     logging.info("Connecting MongoDB...")
#     db.client = AsyncIOMotorClient(local_config.MONGODB_URL,
#                                    maxPoolSize=100,
#                                    minPoolSize=0)
#     logging.info("Connection to MondoDB successful!")
#
#
# async def close_mongo_connection():
#     logging.info("Terminating MongoDB...")
#     db.client.close()
#     logging.info("Terminated MongoDB!")

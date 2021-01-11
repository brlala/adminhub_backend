from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from app.server.conf import settings
from app.server.core.env_variables import local_config

db = AsyncIOMotorClient(local_config.MONGODB_URL, maxPoolSize=100, minPoolSize=0)[local_config.DATABASE_NAME]


def setup_mongodb(app: FastAPI) -> None:
    """
    Helper function to setup MongoDB connection & `motor` client during setup.
    Use during app startup as follows:
    .. code-block:: python
        app = FastAPI()
        @app.on_event('startup')
        async def startup():
            setup_mongodb(app)
    :param app: app object, instance of FastAPI
    :return: None
    """
    client = AsyncIOMotorClient(local_config.MONGODB_URL, minPoolSize=0, maxPoolSize=100)
    app.mongodb = client[local_config.DATABASE_NAME]

#
# class MongoDBClient(object):
#     """
#     Singleton client for interacting with MongoDB.
#     Operates mostly using models, specified when making DB queries.
#     Implements only part of internal `motor` methods, but can be populated more
#     Please don't use it directly, use `fastapi_contrib.db.utils.get_db_client`.
#     """
#
#     __instance = None
#
#     def __new__(cls) -> "MongoDBClient":
#         if cls.__instance is None:
#             cls.__instance = object.__new__(cls)
#             app = get_current_app()
#             tzinfo = get_timezone()
#             cls.__instance.codec_options = CodecOptions(
#                 tz_aware=True, tzinfo=tzinfo)
#             cls.__instance.mongodb = app.mongodb
#         return cls.__instance
#
#     def get_collection(self, collection_name: str) -> Collection:
#         return self.mongodb.get_collection(
#             collection_name, codec_options=self.codec_options)
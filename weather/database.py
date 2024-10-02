from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

mongo_client: AsyncIOMotorClient = AsyncIOMotorClient("mongodb://root:pwd@localhost:27017")
db = mongo_client["weather_db"]


def get_collection(collection_name: str) -> AsyncIOMotorCollection:
    return db[collection_name]

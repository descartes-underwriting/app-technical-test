import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/contactdb")
client = AsyncIOMotorClient(MONGO_URI)
database = client.contactdb
contact_collection = database.get_collection('contacts')

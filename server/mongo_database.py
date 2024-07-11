import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/contactdb")
client = AsyncIOMotorClient(MONGO_URI)
database = client.contactdb
contact_collection = database.get_collection('contacts')
#   nom+prenom forment la clé uniq
contact_collection.create_index([("first_name", 1), ("last_name", 1)], unique=True)

async def clear_database():
    await contact_collection.drop()

# si injection prevoir les functions d'interface
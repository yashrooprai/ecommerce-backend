from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId

MONGO_URI = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URI)
db = client["ecommerce_db"]

# Helper to convert MongoDB's ObjectId to a string
def to_dict(data) -> dict:
    return {**data, "id": str(data["_id"])}

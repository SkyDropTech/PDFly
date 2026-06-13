import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from dotenv import load_dotenv
import certifi

# Load environment variables
load_dotenv()
MONGO_DETAILS = os.getenv("MONGO_URI")

if not MONGO_DETAILS:
    raise ValueError("No MONGO_URI found in .env file.")

# Connect to Atlas
client = AsyncIOMotorClient(MONGO_DETAILS, tlsCAFile=certifi.where())
database = client.pdfly_db

# Collections
users_collection = database.get_collection("users")
conversion_collection = database.get_collection("conversions")

# --- USER QUERIES ---
async def get_user(identifier: str):
    return await users_collection.find_one({
        "$or": [{"email": identifier}, {"username": identifier}]
    })

async def create_user(username: str, email: str, hashed_password: str):
    user = {
        "username": username,
        "email": email, 
        "password": hashed_password, 
        "created_at": datetime.utcnow()
    }
    await users_collection.insert_one(user)
    return True

# --- HISTORY QUERIES ---
async def log_conversion(email: str, filename: str, num_images: int, file_size: str):
    document = {
        "email": email,
        "filename": filename,
        "images_converted": num_images,
        "file_size": file_size,
        "timestamp": datetime.utcnow()
    }
    await conversion_collection.insert_one(document)
    return True

async def get_user_history(email: str):
    cursor = conversion_collection.find({"email": email}).sort("timestamp", -1).limit(50)
    history = await cursor.to_list(length=50)
    
    for doc in history:
        doc["_id"] = str(doc["_id"])
    return history
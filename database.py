import os

from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Fetch the Atlas connection string from .env
MONGO_DETAILS = os.getenv("MONGO_URI")

import certifi
client = AsyncIOMotorClient(MONGO_DETAILS, tlsCAFile=certifi.where())

# Safety check to ensure the URI is loaded
if not MONGO_DETAILS:
    raise ValueError("No MONGO_URI found in .env file. Please ensure your MongoDB Atlas string is added.")

# Create the MongoDB client
# Motor automatically understands the 'mongodb+srv://' protocol used by Atlas
client = AsyncIOMotorClient(MONGO_DETAILS)

# Select the database (Atlas will create this automatically the first time data is inserted)
database = client.pdfly_db

# Select the collection
conversion_collection = database.get_collection("conversions")

async def log_conversion(filename: str, num_images: int, file_size: str):
    """Logs the conversion details to MongoDB Atlas."""
    document = {
        "filename": filename,
        "images_converted": num_images,
        "file_size": file_size,
        "timestamp": datetime.utcnow()
    }
    await conversion_collection.insert_one(document)
    return True
import motor.motor_asyncio
from info import DATABASE_URI, DATABASE_NAME

client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URI)
db = client[DATABASE_NAME]  # Replace with your actual database name
user_settings_collection = db["user_settings"]

async def connection(user_id):
    query = await mycol.find_one(
        { "_id": user_id }
    )
    
    if not query:
        return None

    return query.get('user_settings')
  

import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URI)
db = client[DATABASE_NAME]  # Replace with your actual database name
user_settings_collection = db["user_settings"]


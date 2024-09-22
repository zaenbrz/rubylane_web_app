from itsdangerous import URLSafeTimedSerializer
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient

# Constants
SECRET_KEY = "mysecretkey"
serializer = URLSafeTimedSerializer(SECRET_KEY)

# MongoDB connection details
MONGODB_URL = "mongodb://localhost:27017/"
DATABASE_NAME = "diary"
USERS_COLLECTION_NAME = "users"
ENTRIES_COLLECTION_NAME = "entries"
ADMIN_COLLECTION_NAME = "admin"

client = AsyncIOMotorClient(MONGODB_URL)
db = client[DATABASE_NAME]

# Directory to store uploaded images
UPLOAD_DIRECTORY = Path("static/uploads")
UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)

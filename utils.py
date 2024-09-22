import hashlib
from fastapi import Request, HTTPException, status
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from config import serializer, USERS_COLLECTION_NAME, ADMIN_COLLECTION_NAME, MONGODB_URL, DATABASE_NAME

# Initialize MongoDB client and database
client = AsyncIOMotorClient(MONGODB_URL)
db = client[DATABASE_NAME]

# Function to hash the password
def get_password_hash(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to get current user
async def get_current_user(request: Request):
    session_cookie = request.cookies.get("session")
    if not session_cookie:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    try:
        data = serializer.loads(session_cookie)
        user_id = data.get("user_id")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
        user = await db[USERS_COLLECTION_NAME].find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session")
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session")

# Function to get current admin
async def get_current_admin(request: Request):
    session_cookie = request.cookies.get("admin_session")
    if not session_cookie:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    try:
        data = serializer.loads(session_cookie)
        admin_id = data.get("admin_id")
        if not admin_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
        admin = await db[ADMIN_COLLECTION_NAME].find_one({"_id": ObjectId(admin_id)})
        if not admin:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session")
        return admin
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session")

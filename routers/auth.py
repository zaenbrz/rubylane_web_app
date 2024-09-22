from fastapi import APIRouter, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from itsdangerous import URLSafeTimedSerializer
from config import serializer, SECRET_KEY, db
from utils import get_password_hash


router = APIRouter()
templates = Jinja2Templates(directory="templates")
serializer = URLSafeTimedSerializer(SECRET_KEY)

@router.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = await db["users"].find_one({"username": username})
    if not user or user["hashed_password"] != get_password_hash(password):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})
    session_data = {"user_id": str(user["_id"])}
    session_cookie = serializer.dumps(session_data)
    response = RedirectResponse(url="/diary/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie("session", session_cookie)
    return response

@router.get("/signup", response_class=HTMLResponse)
async def signup_form(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@router.post("/signup", response_class=HTMLResponse)
async def signup(request: Request, username: str = Form(...), password: str = Form(...)):
    user = await db["users"].find_one({"username": username})
    if user:
        return templates.TemplateResponse("signup.html", {"request": request, "error": "Username already taken"})
    
    hashed_password = get_password_hash(password)
    new_user = {
        "username": username,
        "hashed_password": hashed_password
    }
    result = await db["users"].insert_one(new_user)
    user_id = result.inserted_id

    session_data = {"user_id": str(user_id)}
    session_cookie = serializer.dumps(session_data)
    response = RedirectResponse(url="/diary/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie("session", session_cookie)
    return response

@router.get("/logout")
async def logout(request: Request):
    response = RedirectResponse(url="/")
    response.delete_cookie("session")
    return response

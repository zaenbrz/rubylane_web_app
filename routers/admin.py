from fastapi import APIRouter, Request, Form, HTTPException, status, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from bson import ObjectId
from config import SECRET_KEY, db
from utils import get_password_hash, get_current_admin
from itsdangerous import URLSafeTimedSerializer

router = APIRouter()
templates = Jinja2Templates(directory="templates")
serializer = URLSafeTimedSerializer(SECRET_KEY)

@router.get("/admin/login", response_class=HTMLResponse)
async def admin_login_form(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})

@router.post("/admin/login", response_class=HTMLResponse)
async def admin_login(request: Request, username: str = Form(...), password: str = Form(...)):
    admin = await db["admin"].find_one({"username": username})
    if not admin or admin["hashed_password"] != get_password_hash(password):
        return templates.TemplateResponse("admin_login.html", {"request": request, "error": "Invalid credentials"})
    session_data = {"admin_id": str(admin["_id"])}
    session_cookie = serializer.dumps(session_data)
    response = RedirectResponse(url="/admin/admin/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie("admin_session", session_cookie)
    return response

@router.get("/admin/dashboard", response_class=HTMLResponse)
async def admin_panel(request: Request):
    users = await db["users"].find().to_list(length=None)
    return templates.TemplateResponse("admin_panel.html", {"request": request, "users": users})

@router.post("/admin/user/delete/{user_id}")
async def delete_user(user_id: str, admin: dict = Depends(get_current_admin)):
    result = await db["users"].delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    await db["entries"].delete_many({"user_id": ObjectId(user_id)})
    return RedirectResponse(url="/admin/admin/dashboard", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/admin/logout")
async def admin_logout(request: Request):
    response = RedirectResponse(url="/")
    response.delete_cookie("admin_session")
    return response

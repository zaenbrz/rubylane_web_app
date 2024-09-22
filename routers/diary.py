from fastapi import APIRouter, Request, Depends, Form, UploadFile, File, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from bson import ObjectId
from pathlib import Path
from uuid import uuid4
from config import db
from utils import get_current_user


router = APIRouter()
templates = Jinja2Templates(directory="templates")
UPLOAD_DIRECTORY = Path("static/uploads")

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, user: dict = Depends(get_current_user)):
    entries_cursor = db["entries"].find({"user_id": str(user["_id"])})
    entries = await entries_cursor.to_list(length=None)
    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "username": user["username"], "entries": entries}
    )

@router.get("/add_entry", response_class=HTMLResponse)
async def add_entry_form(request: Request):
    return templates.TemplateResponse("add_entry.html", {"request": request})

@router.post("/add_entry", response_class=HTMLResponse)
async def add_entry(
    request: Request, 
    title: str = Form(...), 
    content: str = Form(...), 
    file: UploadFile = File(None), 
    user: dict = Depends(get_current_user)
):
    entry = {"user_id": str(user["_id"]), "title": title, "content": content, "image_path": None}
    if file and file.filename:
        file_extension = file.filename.split(".")[-1]
        file_name = f"{uuid4()}.{file_extension}"
        file_path = UPLOAD_DIRECTORY / file_name
        with file_path.open("wb") as f:
            f.write(await file.read())
        entry["image_path"] = f"/static/uploads/{file_name}"
    await db["entries"].insert_one(entry)
    return RedirectResponse(url="/diary/dashboard", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/edit_entry/{entry_id}", response_class=HTMLResponse)
async def edit_entry_form(request: Request, entry_id: str, user: dict = Depends(get_current_user)):
    entry = await db["entries"].find_one({"_id": ObjectId(entry_id), "user_id": str(user["_id"])})
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found")
    return templates.TemplateResponse("edit_entry.html", {"request": request, "entry": entry})

@router.post("/edit_entry/{entry_id}", response_class=HTMLResponse)
async def edit_entry(
    request: Request, 
    entry_id: str, 
    title: str = Form(...), 
    content: str = Form(...), 
    file: UploadFile = File(None), 
    user: dict = Depends(get_current_user)
):
    entry = await db["entries"].find_one({"_id": ObjectId(entry_id), "user_id": str(user["_id"])})
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found")
    updated_entry = {"title": title, "content": content}
    if file and file.filename:
        file_extension = file.filename.split(".")[-1]
        file_name = f"{uuid4()}.{file_extension}"
        file_path = UPLOAD_DIRECTORY / file_name
        with file_path.open("wb") as f:
            f.write(await file.read())
        updated_entry["image_path"] = f"/static/uploads/{file_name}"
        if entry.get("image_path"):
            old_file_path = UPLOAD_DIRECTORY / entry["image_path"].split("/")[-1]
            if old_file_path.exists():
                old_file_path.unlink()
    else:
        updated_entry["image_path"] = entry.get("image_path")
    await db["entries"].update_one({"_id": ObjectId(entry_id)}, {"$set": updated_entry})
    return RedirectResponse(url="/diary/dashboard", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/delete_entry/{entry_id}", response_class=JSONResponse)
async def delete_entry(entry_id: str, user: dict = Depends(get_current_user)):
    entry = await db["entries"].find_one({"_id": ObjectId(entry_id), "user_id": str(user["_id"])})
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found")
    if entry.get("image_path"):
        file_path = UPLOAD_DIRECTORY / entry["image_path"].split("/")[-1]
        if file_path.exists():
            file_path.unlink()
    await db["entries"].delete_one({"_id": ObjectId(entry_id)})
    return JSONResponse(content={"success": True})

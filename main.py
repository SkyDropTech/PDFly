import os
import shutil
import uuid
from typing import List
from fastapi import FastAPI, UploadFile, File, Form, Request, Depends, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer
from starlette.background import BackgroundTask
import jwt
import bcrypt
from datetime import datetime, timedelta

from converter import PDFConverter
from database import log_conversion, get_user, create_user, get_user_history

app = FastAPI(title="PDFly Web App")
templates = Jinja2Templates(directory="templates")

# CRITICAL VERCEL FIX: Serverless environments require using the /tmp directory
TEMP_DIR = "/tmp/temp_conversions"
os.makedirs(TEMP_DIR, exist_ok=True)

# ==========================================
# AUTHENTICATION SETUP
# ==========================================
SECRET_KEY = "pdfly-super-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return email
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Session expired. Please log in again.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid session token.")

# ==========================================
# ROUTES
# ==========================================
def cleanup_temp_files(folder_path: str):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

@app.get("/", response_class=HTMLResponse)
async def serve_frontend(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/signup")
async def signup(username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    if await get_user(email) or await get_user(username):
        return JSONResponse(status_code=400, content={"error": "Username or Email already registered"})
    
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    await create_user(username, email, hashed_pwd)
    return {"message": "Account created successfully"}

@app.post("/login")
async def login(identifier: str = Form(...), password: str = Form(...)):
    user = await get_user(identifier)
    
    is_valid_password = False
    if user:
        try:
            is_valid_password = bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8'))
        except Exception:
            pass

    if not user or not is_valid_password:
        return JSONResponse(status_code=401, content={"error": "Invalid username/email or password"})
    
    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "username": user["username"], "email": user["email"]}

@app.get("/history")
async def history(email: str = Depends(get_current_user)):
    user_history = await get_user_history(email)
    return {"history": user_history}

@app.post("/convert")
async def convert_images_to_pdf(
    email: str = Depends(get_current_user),
    files: List[UploadFile] = File(...),
    filename: str = Form(...)
):
    session_id = str(uuid.uuid4())
    session_dir = os.path.join(TEMP_DIR, session_id)
    os.makedirs(session_dir, exist_ok=True)
    image_paths = []
    
    try:
        for file in files:
            file_path = os.path.join(session_dir, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            image_paths.append(file_path)
            
        if not filename.lower().endswith('.pdf'):
            filename += '.pdf'
            
        output_pdf_path = os.path.join(session_dir, filename)
        PDFConverter.convert(image_paths, output_pdf_path)
        
        pdf_size = PDFConverter.get_pdf_size(output_pdf_path)
        await log_conversion(email, filename, len(image_paths), pdf_size)
        
        return FileResponse(
            path=output_pdf_path, 
            filename=filename,
            media_type="application/pdf",
            background=BackgroundTask(cleanup_temp_files, session_dir)
        )
    except Exception as e:
        cleanup_temp_files(session_dir)
        return JSONResponse(status_code=500, content={"error": str(e)})
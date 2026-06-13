import os
import shutil
import uuid
from typing import List
from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.background import BackgroundTask

# Import your existing converter logic and the new database logger
from converter import PDFConverter
from database import log_conversion

app = FastAPI(title="PDFly Web App")

# Set up templates directory to serve the frontend
templates = Jinja2Templates(directory="templates")

# Temporary storage for conversions to avoid cluttering your main folder
TEMP_DIR = "temp_conversions"
os.makedirs(TEMP_DIR, exist_ok=True)

def cleanup_temp_files(folder_path: str):
    """Deletes the temporary folder after the PDF is successfully sent to the user."""
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

@app.get("/", response_class=HTMLResponse)
async def serve_frontend(request: Request):
    """Serves the main web interface (index.html)."""
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/convert")
async def convert_images_to_pdf(
    files: List[UploadFile] = File(...),
    filename: str = Form(...)
):
    """Receives images, converts them to PDF, logs to DB, and returns the file."""
    
    # 1. Create a unique folder for this specific user's conversion
    session_id = str(uuid.uuid4())
    session_dir = os.path.join(TEMP_DIR, session_id)
    os.makedirs(session_dir, exist_ok=True)
    
    image_paths = []
    
    try:
        # 2. Save the uploaded images temporarily
        for file in files:
            file_path = os.path.join(session_dir, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            image_paths.append(file_path)
            
        # 3. Ensure the output filename ends with .pdf
        if not filename.lower().endswith('.pdf'):
            filename += '.pdf'
            
        output_pdf_path = os.path.join(session_dir, filename)
        
        # 4. Use your existing Python logic to stitch the images into a PDF
        PDFConverter.convert(image_paths, output_pdf_path)
        
        # 5. Log the conversion metadata to MongoDB
        pdf_size = PDFConverter.get_pdf_size(output_pdf_path)
        await log_conversion(filename, len(image_paths), pdf_size)
        
        # 6. Send the finalized PDF back and delete the temp files AFTER download completes
        return FileResponse(
            path=output_pdf_path, 
            filename=filename,
            media_type="application/pdf",
            background=BackgroundTask(cleanup_temp_files, session_dir)
        )
        
    except Exception as e:
        # If anything crashes, clean up the messy files immediately
        cleanup_temp_files(session_dir)
        # 7. CRITICAL FIX: Send a 500 error code so the browser knows it failed
        return JSONResponse(status_code=500, content={"error": str(e)})
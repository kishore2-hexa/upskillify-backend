from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import SessionLocal
from models import ResumeUpload
import os
from datetime import datetime

import asyncio
from database import engine
from models import Base

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)



# Dependency to get DB session
async def get_db():
    async with SessionLocal() as session:
        yield session

@app.get("/")
def root():
    return {"message": "FastAPI is working!"}

@app.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)  # ✅ Inject DB session
):
    # ✅ Check file type
    if file.content_type not in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are allowed")

    # ✅ Save file to disk
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # ✅ Save metadata to DB
    new_resume = ResumeUpload(
        filename=filename,
        file_path=file_path,
        content_type=file.content_type,
        uploaded_at=datetime.utcnow()
    )
    db.add(new_resume)
    await db.commit()

    return JSONResponse(status_code=200, content={
        "filename": filename,
        "message": "Resume uploaded and saved in DB",
        "file_path": file_path
    })


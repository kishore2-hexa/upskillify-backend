from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class ResumeUpload(Base):
    __tablename__ = "resume_uploads"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(255), nullable=False)
    content_type = Column(String(100))
    uploaded_at = Column(DateTime, default=datetime.utcnow)

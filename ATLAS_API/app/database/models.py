from .database import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy import text

class Files(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True)
    file_id = Column(String)
    file_unique_id = Column(String)
    file_name = Column(String)
    url = Column(String)
    file_type = Column(String)
    uploaded_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

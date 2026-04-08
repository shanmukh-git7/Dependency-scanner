from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="user")  # 'user' or 'admin'
    reset_token = Column(String, nullable=True)
    reset_token_expiry = Column(DateTime, nullable=True)

    scans = relationship("ScanResult", back_populates="owner")

class ScanResult(Base):
    __tablename__ = "scan_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    filename = Column(String)
    scan_date = Column(DateTime, default=datetime.utcnow)
    total_dependencies = Column(Integer)
    vulnerabilities_count = Column(Integer)
    details = Column(String)  # Storing JSON as string for simplicity in SQLite

    owner = relationship("User", back_populates="scans")

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    role: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str

class TokenData(BaseModel):
    username: Optional[str] = None

class ScanResultBase(BaseModel):
    filename: str
    total_dependencies: int
    vulnerabilities_count: int
    details: str

class ScanResultResponse(ScanResultBase):
    id: int
    scan_date: datetime
    user_id: int

    class Config:
        from_attributes = True

class ForgotPasswordRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    otp: str
    new_password: str

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta, datetime
import secrets
import random
from .. import models, schemas, database, auth

router = APIRouter(tags=["Authentication"])

@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Assign admin role if username is 'admin' (case-insensitive for safety, though implementation uses exact match usually)
    role = "admin" if user.username.lower() == "admin" else "user"
    
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "role": user.role}

@router.post("/forgot-password")
def forgot_password(request: schemas.ForgotPasswordRequest, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user:
        # For security reasons, don't reveal if email exists, but in a demo we might want more clarity
        return {"message": "If your email is registered, you will receive an OTP."}
    
    otp = str(random.randint(100000, 999999))
    user.reset_token = otp
    user.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)
    db.commit()
    
    from ..utils.email_utils import send_otp_email
    email_sent = send_otp_email(request.email, otp)
    
    if email_sent:
        return {
            "message": "If your email is registered, an OTP has been securely sent."
        }
    else:
        return {
            "message": "OTP generated, but email delivery failed (Check server logs or .env config)."
        }

@router.post("/reset-password")
def reset_password(request: schemas.ResetPasswordRequest, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.reset_token == request.otp,
        models.User.reset_token_expiry > datetime.utcnow()
    ).first()
    
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    
    user.hashed_password = auth.get_password_hash(request.new_password)
    user.reset_token = None
    user.reset_token_expiry = None
    db.commit()
    
    return {"message": "Password updated successfully"}

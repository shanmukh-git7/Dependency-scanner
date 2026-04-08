from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database, auth

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/users", response_model=List[schemas.UserResponse])
def get_all_users(current_user: models.User = Depends(auth.get_current_admin_user), db: Session = Depends(database.get_db)):
    return db.query(models.User).all()

@router.delete("/users/{id}")
def delete_user(id: int, current_user: models.User = Depends(auth.get_current_admin_user), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")
        
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}

@router.get("/scans", response_model=List[schemas.ScanResultResponse])
def get_all_scans(current_user: models.User = Depends(auth.get_current_admin_user), db: Session = Depends(database.get_db)):
    return db.query(models.ScanResult).all()

@router.delete("/scans/{id}")
def delete_scan_admin(id: int, current_user: models.User = Depends(auth.get_current_admin_user), db: Session = Depends(database.get_db)):
    scan = db.query(models.ScanResult).filter(models.ScanResult.id == id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    db.delete(scan)
    db.commit()
    return {"message": "Scan deleted"}

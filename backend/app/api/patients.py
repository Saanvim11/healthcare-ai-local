from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from backend.app.db.database import get_db
from backend.app.models.user import User
from backend.app.core.config import settings

router = APIRouter(prefix="/patients", tags=["Patients"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user


@router.post("/")
def create_patient(patient_data: dict, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return {"message": "Patient record created successfully", "doctor": current_user.full_name}


@router.get("/me")
def get_my_profile(current_user = Depends(get_current_user)):
    return {
        "full_name": current_user.full_name,
        "role": current_user.role,
        "email": current_user.email
    }
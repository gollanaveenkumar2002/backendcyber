"""
Authentication API - Signup and Login
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import jwt, JWTError
import os
from dotenv import load_dotenv

from database import get_db
from models import Admin

load_dotenv()

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter(prefix="/api/auth", tags=["Authentication"])
security = HTTPBearer()


# ===== PYDANTIC SCHEMAS =====

class SignupRequest(BaseModel):
    username: str
    password: str
    full_name: str


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str


class AdminResponse(BaseModel):
    id: int
    username: str
    full_name: str
    
    class Config:
        from_attributes = True


# ===== HELPER FUNCTIONS =====

def create_access_token(data: dict):
    """Create JWT token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Admin:
    """Get current authenticated admin from token"""
    token = credentials.credentials
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        admin_id = payload.get("sub")
        if not admin_id:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    admin = db.query(Admin).filter(Admin.id == int(admin_id)).first()
    if not admin:
        raise HTTPException(status_code=401, detail="Admin not found")
    
    return admin


# ===== API ENDPOINTS =====

@router.post("/signup", response_model=TokenResponse)
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    """
    Create new admin account
    
    Request body:
    - username: Unique username
    - password: Password (plain text)
    - full_name: Full name of admin
    """
    # Check if username exists
    existing = db.query(Admin).filter(Admin.username == request.username).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    # Create new admin
    admin = Admin(
        username=request.username,
        password=request.password,  # Plain text storage
        full_name=request.full_name
    )
    
    db.add(admin)
    db.commit()
    db.refresh(admin)
    
    # Generate token
    access_token = create_access_token(data={"sub": str(admin.id)})
    
    return TokenResponse(
        access_token=access_token,
        username=admin.username
    )


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Login with username and password
    
    Request body:
    - username: Admin username
    - password: Admin password
    """
    # Find admin
    admin = db.query(Admin).filter(Admin.username == request.username).first()
    
    # Verify credentials
    if not admin or admin.password != request.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # Generate token
    access_token = create_access_token(data={"sub": str(admin.id)})
    
    return TokenResponse(
        access_token=access_token,
        username=admin.username
    )


@router.get("/me", response_model=AdminResponse)
def get_me(admin: Admin = Depends(get_current_admin)):
    """Get current admin profile"""
    return admin

"""
Image Upload API
Handles image uploads and returns URLs for use in blog posts
"""
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from pydantic import BaseModel
import os
import uuid
from pathlib import Path

from auth import get_current_admin
from models import Admin

router = APIRouter(prefix="/api/upload", tags=["Image Upload"])

# Configuration
UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
ALLOWED_MIME_TYPES = {
    "image/jpeg",
    "image/jpg", 
    "image/png",
    "image/gif",
    "image/webp"
}

# Ensure upload directory exists
Path(UPLOAD_DIR).mkdir(exist_ok=True)


# ===== PYDANTIC SCHEMAS =====

class ImageUploadResponse(BaseModel):
    url: str
    filename: str
    size: int


# ===== HELPER FUNCTIONS =====

def validate_image(file: UploadFile) -> None:
    """
    Validate uploaded file
    Checks file type and size
    """
    # Check MIME type
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_MIME_TYPES)}"
        )
    
    # Check file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file extension. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )


def generate_unique_filename(original_filename: str) -> str:
    """
    Generate unique filename using UUID
    Preserves original file extension
    """
    file_ext = Path(original_filename).suffix.lower()
    unique_name = f"{uuid.uuid4()}{file_ext}"
    return unique_name


# ===== API ENDPOINTS =====

@router.post("", response_model=ImageUploadResponse)
async def upload_image(
    file: UploadFile = File(...),
    admin: Admin = Depends(get_current_admin)
):
    """
    Upload image file (Admin only)
    
    - Accepts: JPEG, PNG, GIF, WebP
    - Max size: 10MB
    - Returns URL to use in blog posts
    
    Example response:
    {
        "url": "http://localhost:8000/uploads/12345-abcd.jpg",
        "filename": "12345-abcd.jpg",
        "size": 245678
    }
    """
    # Validate file
    validate_image(file)
    
    # Read file content
    file_content = await file.read()
    file_size = len(file_content)
    
    # Check file size
    if file_size > MAX_FILE_SIZE:
        max_mb = MAX_FILE_SIZE / (1024 * 1024)
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Maximum size: {max_mb}MB"
        )
    
    # Generate unique filename
    unique_filename = generate_unique_filename(file.filename)
    file_path = Path(UPLOAD_DIR) / unique_filename
    
    # Save file
    try:
        with open(file_path, "wb") as f:
            f.write(file_content)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file: {str(e)}"
        )
    
    # Generate URL
    # In production, replace with your actual domain
    url = f"http://localhost:8000/uploads/{unique_filename}"
    
    return ImageUploadResponse(
        url=url,
        filename=unique_filename,
        size=file_size
    )


@router.get("/list")
def list_uploaded_images(admin: Admin = Depends(get_current_admin)):
    """
    List all uploaded images (Admin only)
    
    Returns list of uploaded image filenames
    """
    upload_path = Path(UPLOAD_DIR)
    
    if not upload_path.exists():
        return {"images": []}
    
    images = []
    for file_path in upload_path.iterdir():
        if file_path.is_file():
            images.append({
                "filename": file_path.name,
                "url": f"http://localhost:8000/uploads/{file_path.name}",
                "size": file_path.stat().st_size
            })
    
    return {"images": images}

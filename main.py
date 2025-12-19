"""
Cyber Anytime - Main Application
Clean and simple FastAPI backend
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

# Import routers
from auth import router as auth_router
from blog import router as blog_router
from image import router as image_router

# Create uploads directory if it doesn't exist
UPLOAD_DIR = "uploads"
Path(UPLOAD_DIR).mkdir(exist_ok=True)

# Create FastAPI app
app = FastAPI(
    title="Cyber Anytime API",
    version="1.0.0",
    description="""
    ## Cyber Anytime Backend
    
    Simple API for admin authentication, blog management, and image uploads.
    
    ### Endpoints:
    
    **Authentication:**
    - POST /api/auth/signup - Create admin account
    - POST /api/auth/login - Login with username/password
    - GET /api/auth/me - Get current admin (requires token)
    
    **Blog Posts:**
    - POST /api/blog - Create blog post (admin only)
    - GET /api/blog - Get all blog posts (public)
    - GET /api/blog/{id} - Get single blog post (public)
    - PUT /api/blog/{id} - Update blog post (admin only)
    - DELETE /api/blog/{id} - Delete blog post (admin only)
    
    **Image Upload:**
    - POST /api/upload - Upload image (admin only)
    - GET /api/upload/list - List uploaded images (admin only)
    
    ### Database Tables:
    - **admins**: id, username, password, full_name
    - **blog_posts**: id, title, content, media_url, author_name
    """
)

# CORS middleware - Allow all origins (configure for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount uploads folder as static files
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Include routers
app.include_router(auth_router)
app.include_router(blog_router)
app.include_router(image_router)


# Root endpoint
@app.get("/")
def root():
    """Health check"""
    return {
        "status": "online",
        "message": "Cyber Anytime API is running",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

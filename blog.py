"""
Blog Post API - Create, Read, Update, Delete
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

from database import get_db
from models import BlogPost, Admin
from auth import get_current_admin

router = APIRouter(prefix="/api/blog", tags=["Blog Posts"])


# ===== PYDANTIC SCHEMAS =====

class BlogPostCreate(BaseModel):
    title: str
    content: str
    media_url: Optional[str] = None
    author_name: str


class BlogPostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    media_url: Optional[str] = None
    author_name: Optional[str] = None


class BlogPostResponse(BaseModel):
    id: int
    title: str
    content: str
    media_url: Optional[str]
    author_name: str
    
    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    message: str


# ===== API ENDPOINTS =====

@router.post("", response_model=BlogPostResponse, status_code=status.HTTP_201_CREATED)
def create_blog_post(
    post: BlogPostCreate,
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin)
):
    """
    Create new blog post (Admin only)
    
    Request body:
    - title: Post title
    - content: Post content
    - media_url: Optional media URL
    - author_name: Author name (any string)
    """
    blog_post = BlogPost(
        title=post.title,
        content=post.content,
        media_url=post.media_url,
        author_name=post.author_name
    )
    
    db.add(blog_post)
    db.commit()
    db.refresh(blog_post)
    
    return blog_post


@router.get("", response_model=List[BlogPostResponse])
def get_all_blog_posts(db: Session = Depends(get_db)):
    """
    Get all blog posts (Public)
    
    Returns list of all blog posts
    """
    posts = db.query(BlogPost).all()
    return posts


@router.get("/{post_id}", response_model=BlogPostResponse)
def get_blog_post(post_id: int, db: Session = Depends(get_db)):
    """
    Get single blog post by ID (Public)
    
    Path parameter:
    - post_id: Blog post ID
    """
    post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog post not found"
        )
    
    return post


@router.put("/{post_id}", response_model=BlogPostResponse)
def update_blog_post(
    post_id: int,
    post_data: BlogPostUpdate,
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin)
):
    """
    Update blog post (Admin only)
    
    Path parameter:
    - post_id: Blog post ID to update
    
    Request body:
    - title: Optional new title
    - content: Optional new content
    - media_url: Optional new media URL
    - author_name: Optional new author name
    """
    post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog post not found"
        )
    
    # Update fields if provided
    if post_data.title is not None:
        post.title = post_data.title
    if post_data.content is not None:
        post.content = post_data.content
    if post_data.media_url is not None:
        post.media_url = post_data.media_url
    if post_data.author_name is not None:
        post.author_name = post_data.author_name
    
    db.commit()
    db.refresh(post)
    
    return post


@router.delete("/{post_id}", response_model=MessageResponse)
def delete_blog_post(
    post_id: int,
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin)
):
    """
    Delete blog post (Admin only)
    
    Path parameter:
    - post_id: Blog post ID to delete
    """
    post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog post not found"
        )
    
    db.delete(post)
    db.commit()
    
    return MessageResponse(message=f"Blog post '{post.title}' deleted successfully")

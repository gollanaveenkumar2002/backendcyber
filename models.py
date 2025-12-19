"""
Database Models
Defines the structure of database tables
"""
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

# Base class for all models
Base = declarative_base()


class Admin(Base):
    """
    Admin table - stores admin user credentials
    
    Columns:
    - id: Auto-increment primary key
    - username: Unique username for login
    - password: Plain text password
    - full_name: Admin's full name
    """
    __tablename__ = "admins"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    
    def __repr__(self):
        return f"<Admin(id={self.id}, username='{self.username}')>"


class BlogPost(Base):
    """
    Blog posts table - stores blog content
    
    Columns:
    - id: Auto-increment primary key
    - title: Blog post title
    - content: Blog post content (text)
    - media_url: Optional URL to media (image/video)
    - author_name: Author name (simple string, not a foreign key)
    """
    __tablename__ = "blog_posts"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    media_url = Column(String(500), nullable=True)
    author_name = Column(String(255), nullable=False)
    
    def __repr__(self):
        return f"<BlogPost(id={self.id}, title='{self.title}')>"
